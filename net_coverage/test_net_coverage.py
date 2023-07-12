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
        coverage_file_path = os.path.join(net_coverage_dir, 'data/test/insert_prov_coverage.json')
        response_coverage_path = os.path.join(net_coverage_dir, 'data/test/response_coverage.json')
        with open(coverage_file_path) as cv_file:
            coverage_dict = json.load(cv_file)
        new_prov_coverage = ProvidersCoverage.objects.create(**coverage_dict)
        self.post_code = new_prov_coverage.post_code
        self.city_name = "Ouessant"
        with open(response_coverage_path) as rs_file:
            self.coverage_response_data = json.load(rs_file).get("data")

    def test_GetNetworkCoverage(self):
        request = self.factory.get(
            f'/net_coverage/GetNetworkCoverage/?city_name={self.city_name}&post_code={self.post_code}')
        response = GetNetworkCoverage.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, self.coverage_response_data)

