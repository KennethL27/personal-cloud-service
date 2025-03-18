# personal-cloud-service

## About this Project

This project aims to create an in-house solution for uploading personal files such as photos, videos, and pdf files to a external hard drive 
that is hosted on a house hold router. The traffic in and out of the hard drive will be hosted on a raspberry pi.

## Built With

- FastAPI
- Pytest
- Uvicorn
 
## Getting Started

In order to run this app locally please follow these commands
```
~ python -m venv venv
~ pip install .
~ uvicorn src.main:app --reload
```

## Test Coverage

This app uses pytest for its test suite. 
To run all tests use `pytest` and to run specific test file use `pytest tests/path/to/file.py`.
To run single test scenarios use the following method `pytest tests/path/to/file.py::TestClassName::test_scenario`
