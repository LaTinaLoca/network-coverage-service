import requests
from decouple import config


class AddressIngestion:
    def __init__(self):
        self.address_base_url = config("ADDRESS_INGESTION_BASE_URL")

    def get_address_from_coordinates(self, latitude, longitude, limit=1):
        address = []
        err_msg = ""
        url = f"{self.address_base_url}/reverse/"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "lon": longitude,
            "lat": latitude,
            "limit": limit
        }
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code == 200:
            address = response.json()["features"]
        else:
            err_msg = f"Error in get_address_from_coordinates for params {params}: {response.text}"
        return address, err_msg

    def search_address(self, query, post_code=None, limit=1):
        # Examples:
        # https: // api - adresse.data.gouv.fr / search /?q = 8 + bd + du + port + amiens & limit = 1
        # https: // api - adresse.data.gouv.fr / search /?q = paris & type = street & postcode=44380
        address = []
        err_msg = ""
        url = f"{self.address_base_url}/search/"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            "q": query,
            "postcode": post_code,
            "limit": limit
        }

        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code == 200:
            address = response.json()["features"]
        else:
            err_msg = f"Error in search_address for params {params}: {response.text}"
        return address, err_msg

    @staticmethod
    def get_postcode_citycode_from_address(address_from_gov_api):
        post_code = None
        city_code = None
        if address_from_gov_api and isinstance(address_from_gov_api, dict):
            properties = address_from_gov_api.get("properties", False)
            if properties:
                post_code = properties.get("postcode", None)
                city_code = properties.get("citycode", None)
        return post_code, city_code
