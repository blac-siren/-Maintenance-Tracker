https://travis-ci.org/blac-siren/Maintenance-Tracker.svg?branch=deployment
# Maintenance-Tracker


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
$ source .venv/bin/activate
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

| url | Method|  Description 
| --- | --- | --- 
| /api-v1/register | POST | Registers new user 
| /api-v1/login | POST | Handles POST request for /login
| /api-v1/users/requests | GET | Get every requests of logged in user
| /api-v1/users/requests/{id} | GET | Gets one of request 
| /api-v1/users/requests | POST | Create a new request
| /api-v1/users/requests/{requestId}  | PUT | Update an existing request
| /api-v1/users/requests/{requestId} | DELETE | Delete request by id


