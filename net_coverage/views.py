from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from .serializers import GetNetworkCoverageSerializer


class GetNetworkCoverage(APIView):
    serializer_class = GetNetworkCoverageSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='address', location=OpenApiParameter.QUERY,
                             description='address to get the coverage of: number, street, zip code, city format',
                             required=True, type=str)
        ], summary="Get network coverage for an address",
        description="It returns the network coverage (2G/3G/4G) of a given address based on the "
                    "phone providers availability")
    def get(self, request, *args, **kwargs):
        address = request.GET.get("address")
        return Response({"address": address}, status=200)
