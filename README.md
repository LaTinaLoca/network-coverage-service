# Network Coverage

Network Coverage is a Python API service which takes care of returning the network coverage (2G/3G/4G) on the French territory 
of the main phone providers. Providing an address in the request
the service returns the coverage for each available provider. The coverage is provided at city-level (city_code INSEE used).

Request formats:
1) either the whole address in the format like address=52 Route de Brest post_code=29830 city_name=Ploudalmézeau
2) or just post code and city name like post_code=29830 city_name=Ploudalmézeau
3) or address and city name like address=52 Route de Brest city_name=Ploudalmézeau
4) simply the post code like post_code=29830

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
so, alternatively, for the sake of testing the service out-of-the-box, the already populated 
net_coverage.sqlite3 file can be used which contains all the basic Django data as well as the 
pre-populated providers data.

## Execution
1. Create .env file with your environment configuration.

2. Run a local server with:
```bash
  python manage.py runserver
```

### Swagger API Link
1. localhost:8000/api/v1/schema/swagger-ui/
2. localhost:8000/api/v1/schema/redoc/