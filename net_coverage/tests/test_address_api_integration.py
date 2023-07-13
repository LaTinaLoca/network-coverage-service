import os
import json
from pathlib import Path
from django.test import TestCase
from unittest.mock import patch
from net_coverage.utilities.address_ingestion import AddressIngestion

net_coverage_dir = Path(__file__).resolve().parent
search_api_response_path = os.path.join(net_coverage_dir, 'test_data/search_api_response.json')
with open(search_api_response_path) as search_file:
    search_api_response = json.load(search_file).get("features")
reverse_api_response_path = os.path.join(net_coverage_dir, 'test_data/reverse_api_response.json')
with open(reverse_api_response_path) as reverse_file:
    reverse_api_response = json.load(reverse_file).get("features")


class SearchMockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return search_api_response, ""


class ReverseMockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return reverse_api_response, ""


class TestAddressApiIntegration(TestCase):
    @patch("requests.get", return_value=SearchMockResponse())
    def test_search_api(self, mocked):
        search_resp, err_msg = AddressIngestion().search_address(query="29242")
        self.assertEqual(
            search_resp,
            search_api_response
        )
        self.assertEqual(
            err_msg,
            ""
        )

    @patch("requests.get", return_value=ReverseMockResponse())
    def test_reverse_api(self, mocked):
        reverse_response, err_msg = AddressIngestion().get_address_from_coordinates(
            latitude=48.528795, longitude=-4.660348)
        self.assertEqual(
            reverse_response,
            reverse_api_response
        )
        self.assertEqual(
            err_msg,
            ""
        )

    @patch("requests.get", return_value=ReverseMockResponse())
    def test_bad_reverse_api_request(self, mocked):
        reverse_response, err_msg = AddressIngestion().get_address_from_coordinates(
            latitude="aaa", longitude=-270)
        self.assertEqual(
            reverse_response,
            []
        )

    @patch("requests.get", return_value=ReverseMockResponse())
    def test_bad_search_api_request(self, mocked):
        search_response, err_msg = AddressIngestion().search_address(
            query="")
        self.assertEqual(
            search_response,
            []
        )

    def test_get_postcode_citycode_from_address(self):
        post_code, city_code = AddressIngestion().get_postcode_citycode_from_address(
            address_from_gov_api=search_api_response[0])
        self.assertEqual(post_code, "29242")
        self.assertEqual(city_code, "29155")
        
