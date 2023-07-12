import os
from tqdm import tqdm
from pathlib import Path
import pandas as pd
from decouple import config
from net_coverage.utilities.address_ingestion import AddressIngestion
from net_coverage.utilities.conversion_lambert93_gps import lambert93_to_gps
from net_coverage.serializers import ProvidersCoverageSerializer
from net_coverage.models import ProvidersCoverage
import logging

provider_csv_file_name = config("PROVIDER_CSV_FILE_NAME")
log_file_name = config("LOG_FILE_FULL_NAME")
serializer_class = ProvidersCoverageSerializer
addr_instance = AddressIngestion()
currenct_dir = Path(__file__).resolve().parent
net_coverage_dir = Path(__file__).resolve().parent.parent

logging.basicConfig(filename=os.path.join(currenct_dir, log_file_name),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def data_mapping(row_data):
    data_dict = dict()
    data_dict["provider_mnc"] = int(row_data[int(config("PROVIDER_MNC_COLUMN_NUM"))])
    data_dict["x"] = int(row_data[int(config("PROVIDER_X_COLUMN_NUM"))])
    data_dict["y"] = int(row_data[int(config("PROVIDER_Y_COLUMN_NUM"))])
    lat, lon = lambert93_to_gps(x=data_dict["x"], y=data_dict["y"])
    data_dict["latitude"] = round(lat, 5)
    data_dict["longitude"] = round(lon, 5)
    address, err_msg = addr_instance.get_address_from_coordinates(latitude=lat, longitude=lon)
    if address and isinstance(address, list):
        post_code, city_code = addr_instance.get_postcode_citycode_from_address(address_from_gov_api=address[0])
    else:
        if err_msg:
            logger.error(err_msg)
        logger.warning(f"lat {lat} and lon {lon}: return address {address}")
        # skipping this storage
        return dict()
    data_dict["post_code"] = post_code
    data_dict["city_code"] = city_code
    data_dict["two_g"] = int(row_data[int(config("PROVIDER_2G_COLUMN_NUM"))])
    data_dict["three_g"] = int(row_data[int(config("PROVIDER_3G_COLUMN_NUM"))])
    data_dict["four_g"] = int(row_data[int(config("PROVIDER_4G_COLUMN_NUM"))])
    return data_dict


def csv_parser_and_data_conversion(file_name=provider_csv_file_name):
    full_name = file_name + '.csv'
    full_path = os.path.join(net_coverage_dir, 'data', full_name)
    exists = os.path.isfile(full_path)
    if not exists:
        logger.info(f"Error: the provided file {full_name} doesn't exist under {full_path} path")
        return
    df = pd.read_csv(filepath_or_buffer=full_path, sep=';')
    data_list = []
    for row in tqdm(df.iloc, total=df.shape[0]):
        data_dict = data_mapping(row_data=row)
        serializer = serializer_class(data=data_dict)
        if serializer.is_valid():
            data_list.append(ProvidersCoverage(**data_dict))
    ProvidersCoverage.objects.bulk_create(data_list)


def run():
    csv_parser_and_data_conversion()
