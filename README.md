# Network Coverage

Network Coverage is an API service which takes care fo returning the network coverage (2G/3G/4G) on the French territory 
of the main phone providers. Providing an address in the request (the zip code is enough), the service returns the
coverage for each available provider.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the base requirements
to run the service.
```bash
pip install -r requirements.txt
```

## Execution
Run a local server with
```bash
  python manage.py runserver
```

### Swagger API Link
1. localhost:8000/api/v1/schema/swagger-ui/
2. localhost:8000/api/v1/schema/redoc/