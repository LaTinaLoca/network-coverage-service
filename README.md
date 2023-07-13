# Network Coverage Service

Network Coverage is a Python API service which takes care of returning the network coverage (2G/3G/4G) on the French territory 
of the main phone providers. Providing an address in the request
the service returns the coverage for each available provider. 
The coverage is provided at city-level (city_code INSEE used) so in case of multiple records in the DB for the
same city_code and post_code (but different latitude and longitude coordinates) for the same provider then the 
worst case scenario is considered. 
So, for example, in case of the city Ploudalmézeau (city_code=29178 and post_code=29830), four records are present
in the DB for Bouygues Telecom provider. Two with {2G: True, 3G: True, 4G: True} and two with {2G: True,
3G: True, 4G: False}. The response returned by the API is then 
```json
{
    "provider": "Bouygues Telecom",
    "coverage": {
      "two_g": true,
      "three_g": true,
      "four_g": false
    }
}
```

Example of request to the API service:

GET http://127.0.0.1:8000/net_coverage/api/v1/get-network-coverage/?city_name=Ploudalmézeau

Request formats:
1) either the whole address in the format like address=52 Route de Brest post_code=29830 city_name=Ploudalmézeau
2) or just post code and city name like post_code=29830 city_name=Ploudalmézeau
3) or address and city name like address=52 Route de Brest city_name=Ploudalmézeau
4) simply the post code like post_code=29830
5) simply the city name like city_name=Ploudalmézeau

Example of response:
```json
[
  {
    "provider": "Bouygues Telecom",
    "coverage": {
      "two_g": true,
      "three_g": true,
      "four_g": false
    }
  },
  {
    "provider": "SFR",
    "coverage": {
      "two_g": true,
      "three_g": true,
      "four_g": false
    }
  },
  {
    "provider": "Free mobile",
    "coverage": {
      "two_g": false,
      "three_g": true,
      "four_g": false
    }
  },
  {
    "provider": "Orange",
    "coverage": {
      "two_g": true,
      "three_g": true,
      "four_g": true
    }
  }
]
```
### Prerequisites

You need the following programs installed on your computer:
- Python 3.10+

### Clone the repository

```bash
git clone https://github.com/LaTinaLoca/network-coverage-service.git
cd network-coverage-service
```

### Create a virtual environment

```bash
python3 -m venv venv
```

### Activate the virtual environment

#### Linux / Mac

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the base requirements
to run the service.
```bash
pip install -r requirements.txt
```
The service uses an SQLite DB to store and retrieve network coverage data quickly but there is no need
to install any additional package because it is already integrated in Python.

flake8 and django-extensions packages are optional (the latter for shell_plus availability).

## Initial data ingestion and DB population
1. Create a superuser with the management console
```bash
python manage.py createsuperuser
```
2. Run the migrations to create the basic Django tables 
```bash
python manage.py migrate
```
as well as the provider_coverage table (specific to the Network Coverage Service)
```bash
python manage.py migrate net_coverage
```
3. The provider_coverage table may be populated running 
```bash
python manage.py runscript populate_db_from_csv
```
which ingests all the data present in net_coverage/data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv
file and stores the data coverage converting lambert93 to GPS latitude and
longitude coordinates and adding the city code and the post code information.
Given the size of the .csv file (~77000 rows), the script takes around 3 hours to complete
so, alternatively, for the sake of testing the service, the already populated 
net_coverage.sqlite3 file can be used which contains all the basic Django data as well as the 
pre-populated providers data.
TODO: rename the sqlite3 file to _bck_net_coverage.sqlite3 in case it is not used
and a new DB is created and populated running the populate_db_from_csv script.
Another option is to decide how many records to ingest from the .csv file: a limited number of rows may be
read and stored (like 1000) speeding up the DB population process. 
In this case, naturally, the network coverage service is testable on a restricted
geographic area only given that the DB is missing most of the coverage data across the country.

## Execution
1. Create .env file with your environment configuration.

2. Run a local server with:
```bash
  python manage.py runserver
```

## Testing
There is a suit of unit and integration tests that can be run using
```bash
     python manage.py test net_coverage
```
The installed package [coverage](https://coverage.readthedocs.io/en/7.2.7/) helps check out the testing coverage.
```bash
coverage run manage.py test net_coverage
coverage html
```
The last command generates an html report (under the folder ./htmlcov) that can be inspected opening the index.html file
in a browser to navigate the project test coverage.

### Swagger API Link
1. localhost:8000/api/v1/schema/swagger-ui/
2. localhost:8000/api/v1/schema/redoc/