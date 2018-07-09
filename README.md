[![Build Status](https://travis-ci.org/blac-siren/Maintenance-Tracker.svg?branch=develop)](https://travis-ci.org/blac-siren/Maintenance-Tracker)
[![Coverage Status](https://coveralls.io/repos/github/blac-siren/Maintenance-Tracker/badge.svg?branch=develop&service=github)](https://coveralls.io/github/blac-siren/Maintenance-Tracker?branch=deployment)

# Maintenance-Tracker
Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request

## Prerequisites

Python 2.6 or a later version
Postgresq

## Dependencies
Install all package requirements in your python virtual environment.
```
pip install -r requirements.txt
```
Ensure yourdatabase is up and running on local commandline
in linux : ```service postgresql start```

Create two database called trackerapp and trackertest-used for testing and then create Two table
i.e users and requests. Then navigate your config file and setup a database variable in development and testing
example
``` class DevelopmentConfig(Config):
    """Configuration for development."""

    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:zakaria@localhost/trackerapp')
```

## Env
Create.env file

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

| url | Method|  Description| Authentication |
| --- | --- | --- | --- |
| /api/v1/auth/login | POST | Handles POST request for /auth/login | TRUE
| /api/v1/auth/logout | GET | Logs out a user | TRUE
| /api/v1/auth/register | POST | Registers new user | FALSE
| /api/v1/users/requests | GET | Get every request of logged in user|TRUE
| /api/v1/users/requests/requestId} | GET | Get a request with {id} of logged in user|TRUE
| /api/v1/users/requests | POST | Create a new request|TRUE
| /api/v1/users/requests/requestId} | PUT | Update a request with {id} of logged in user|TRUE
| /api/v1/users/requests/requestId} | DELETE | Delete request with {id} of logged in user|TRUE
| /api/v1/requests | GET | GET all users requests|ADMIN ONLY
| /api/v1/requests/{id}/approve | PUT | Admin approve a pending request|ADMIN ONLY
| /api/v1/requests/{requestId}/disaprove| PUT | Admin disaprove a pending request|ADMIN ONLY
| /api/v1/requests/{requestId}/approve | PUT | Admin resolve request|ADMIN ONLY

## Deployment
http://m-tracker-api.herokuapp.com/

