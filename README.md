[![Build Status](https://travis-ci.org/blac-siren/Maintenance-Tracker.svg?branch=deployment)](https://travis-ci.org/blac-siren/Maintenance-Tracker)
[![Coverage Status](https://coveralls.io/repos/github/blac-siren/Maintenance-Tracker/badge.svg?branch=deployment)](https://coveralls.io/github/blac-siren/Maintenance-Tracker?branch=deployment)

# Maintenance-Tracker
Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request

## Prerequisites

Python 2.6 or a later version

## Dependencies
Install all package requirements in your python virtual environment.
```
pip install -r requirements.txt
```
## Env
Rename .env.sample into .env

## Virtual environment
Activate virtual environment:

```
$ source venv/bin/activate
```

## Testing
To set up unit testing environment:

```
$ pip install nose
```

To execute a test file:

```
$ source .env
$ nosetests
```




### Api endpoints

| URL | Method|  Description 
| --- | --- | --- 
| /api-v1/auth/register | POST | Registers new user 
| /api-v1/auth/login | POST | Handles POST request for login
| /api-v1/users/requests | GET | Get every requests of logged in user
| /api-v1/users/requests/{id} | GET | Gets a request 
| /api-v1/users/requests | POST | Create a new request
| /api-v1/users/requests/{requestId}  | PUT | Update an existing request
| /api-v1/users/requests/{requestId} | DELETE | Delete request by


