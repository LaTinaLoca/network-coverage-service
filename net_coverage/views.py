import re
from unidecode import unidecode
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProvidersCoverage
from .serializers import GetNetworkCoverageSerializer
from net_coverage.utilities.address_ingestion import AddressIngestion
from net_coverage.data.provider_codes import PROVIDERS


class GetNetworkCoverage(APIView):
    serializer_class = GetNetworkCoverageSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='address', location=OpenApiParameter.QUERY,
                             description='street/avenue/square: in the format '
                                         "'52 Route de Brest' (no commas, spaces instead)",
                             required=False, type=str),
            OpenApiParameter(name='post_code', location=OpenApiParameter.QUERY,
                             description="post code of the address: in the format '29830'",
                             required=False, type=str),
            OpenApiParameter(name='city_name', location=OpenApiParameter.QUERY,
                             description="city name of the address: in the format 'Ploudalmézeau'",
                             required=False, type=str),
        ], summary="Get network coverage for an address (at city code level)",
        description="It returns the network coverage (2G/3G/4G) of a given address based on the "
                    "phone providers availability. The info is provided at city code precision level. "
                    "Either the post code or the city name must be " 
                    "provided with the address in the parameters otherwise an error message is returned "
                    "(i.e. too wide search). \n"
                    "Request formats: \n" 
                    "1) all the address info split like address=52 Route de Brest post_code=29830 "
                    "city_name=Ploudalmézeau \n"
                    "2) just post code and city name like post_code=29830 city_name=Ploudalmézeau \n"
                    "3) address and city name like address=52 Route de Brest city_name=Ploudalmézeau \n"
                    "4) simply the post code like post_code=29830 \n"
                    "5) simply the city name like city_name=Ploudalmézeau",
        responses={200: serializer_class()})
    def get(self, request, *args, **kwargs):
        address = unidecode(request.GET.get("address").strip()) if request.GET.get("address") else None
        post_code = request.GET.get("post_code").strip() if request.GET.get("post_code") else None
        city_name = unidecode(request.GET.get("city_name").strip()) if request.GET.get("city_name") else None

        if not post_code and not city_name:
            return Response({"details": "Missing required parameters in the request: please review them. "
                                        "At least one between post_code and city_code must be provided. "
                                        f"Params: address {address} "
                                        f"- post_code {post_code} "
                                        f"- city_name {city_name}"
                             },
                            status=400
                           )
        query = ""
        postcode = None
        simple_address_validation_pattern = "(\\d{1,}) [a-zA-Z0-9\\s]+"
        #whole_address_validation_pattern = "(\\d{1,}) [a-zA-Z0-9\\s]+ [0-9]{5} [a-zA-Z]+"
        postcode_validation_pattern = "[0-9]{5}"
        city_name_validation_pattern = "[a-zA-Z]+"
        if address:
            # whole address is accepted but then I don't append any other info to the query
            if bool(re.fullmatch(simple_address_validation_pattern, address)):
                query += address + " "
            else:
                return Response({"details": f"The provided address {address} doesn't respect the "
                                            "format of num street format like '52 Route de Brest'."},
                                status=400
                                )
        if post_code:
            if bool(re.fullmatch(postcode_validation_pattern, post_code)):
                postcode = post_code
                # using the post_code in the query parameter of the request to the gov API
                # just in case we don't have any other info (like address or city name)
                if not address and not city_name:
                    query = post_code
            else:
                return Response({"details": f"The provided post_code {post_code} doesn't respect the "
                                            "format of 5 digits like '23451'."},
                                status=400
                                )
        if city_name:
            if bool(re.fullmatch(city_name_validation_pattern, city_name)):
                query += city_name
            else:
                return Response({"details": f"The provided city_name {city_name} doesn't respect the "
                                            "alphabetical format like 'Paris'."},
                                status=400
                                )
        addr_instance = AddressIngestion()
        # a list is returned in searched_address
        searched_address, err_msg = addr_instance.search_address(query=query, post_code=postcode)
        # if no response from the governemnt API,
        # returning an error message notifing the user that no address corresponds to the search
        if not searched_address:
            error_detail = f"The provided address parameters didn't resolve in any location findings. " \
                           f"The query used is: q={query}"
            if post_code:
                error_detail += f"&postcode={post_code}. \n"
            if err_msg:
                error_detail += err_msg
            return Response({"details": error_detail},
                            status=400
                            )
        gov_post_code, gov_city_code = addr_instance.get_postcode_citycode_from_address(
                                                                        address_from_gov_api=searched_address[0])
        coverage_objs = None
        if gov_city_code:
            coverage_objs = ProvidersCoverage.objects.filter(
                city_code=int(gov_city_code)
            )
        if not coverage_objs:
            if gov_post_code:
                qs_code = gov_post_code
            elif post_code:
                qs_code = post_code
            else:
                return Response({"details":
                                "There is no post_code nor city_code on which matching the phone provider coverage. "
                                 "Please review the provided parameters and, if correct, retry later."},
                                status=400
                                )
            coverage_objs = ProvidersCoverage.objects.filter(
                post_code=int(qs_code)
            )
            # we don't have the post_code stored: using the city_code if returned by the government API
            if not coverage_objs.exists():
                return Response(
                    {"details": f"There is no post_code {qs_code} nor city_code {gov_city_code} stored "
                                   f"in the DB so no match available on the phone provider coverage. "
                                   "Please review the provided parameters and, if correct, retry later."},
                    status=400)

        unique_providers = coverage_objs.values('provider_mnc').distinct()
        response = []
        for provider in unique_providers:
            per_provider_objs = coverage_objs.filter(
                provider_mnc=provider.get("provider_mnc")
            )
            # for the city code level: conservative approach
            # i.e. if any lat-long point hasn't coverage then that boolean is set to False
            two_g = False if any(not obj.two_g for obj in per_provider_objs) else True
            three_g = False if any(not obj.three_g for obj in per_provider_objs) else True
            four_g = False if any(not obj.four_g for obj in per_provider_objs) else True
            try:
                mapped_dict = dict()
                mapped_dict["provider"] = dict(PROVIDERS)[provider.get("provider_mnc")]
                mapped_dict["coverage"] = {
                    "two_g": two_g,
                    "three_g": three_g,
                    "four_g": four_g
                }
                response.append(mapped_dict)
            except:
                pass
        serializer = self.serializer_class(response, many=True)
        return Response(serializer.data, status=200)
