import os
import json
from pathlib import Path
from django.test import TestCase, RequestFactory
from net_coverage.models import ProvidersCoverage
from net_coverage.views import GetNetworkCoverage

net_coverage_dir = Path(__file__).resolve().parent


class TestNetCoverageApi(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        coverage_file_path = os.path.join(net_coverage_dir, 'test_data/insert_prov_coverage.json')
        response_coverage_path = os.path.join(net_coverage_dir, 'test_data/response_coverage.json')
        with open(coverage_file_path) as cv_file:
            self.coverage_dict = json.load(cv_file)
        with open(response_coverage_path) as rs_file:
            self.coverage_response_data = json.load(rs_file).get("data")

    def test_CreateNetCoverage(self):
        creation_string = "Provider coverage for Orange with coordinates lat 48.45657 and long -5.08885"
        new_prov_coverage = ProvidersCoverage.objects.create(**self.coverage_dict)
        self.assertEqual(str(new_prov_coverage), creation_string)
        self.assertEqual(new_prov_coverage.provider_mnc, 20801)
        self.assertEqual(new_prov_coverage.post_code, 29242)
        self.assertEqual(new_prov_coverage.city_code, 29155)
        self.assertEqual(new_prov_coverage.two_g, True)
        self.assertEqual(new_prov_coverage.three_g, True)
        self.assertEqual(new_prov_coverage.four_g, False)

    def test_GetNetworkCoverage(self):
        self.test_CreateNetCoverage()
        city_name = "Ouessant"
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?city_name={city_name}')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, self.coverage_response_data)

    def test_GetNetworkCoverage_no_post_code_no_city_name(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_GetNetworkCoverage_bad_address(self):
        self.test_CreateNetCoverage()
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?address=3&post_code=12234')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_GetNetworkCoverage_bad_post_code(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?post_code=w34')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_GetNetworkCoverage_bad_city_name(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?city_name=w34')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_GetNetworkCoverage_non_existing_post_code(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?post_code=00023')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_GetNetworkCoverage_concat_query(self):
        self.test_CreateNetCoverage()
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?address=3 Bourg de Lampaul&post_code=29242&city_name=Ouessant')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_GetNetworkCoverage_error_in_search_address(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?city_name=xs')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_GetNetworkCoverage_non_existing_db(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?post_code=29242')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 400)
        








