"""Module for endpoints."""
from flask_restplus import fields, Resource
from app.models.request import CreateRequest
from app.models.user import User
from app import api
from flask import request, jsonify, abort, make_response, abort
from flask_bcrypt import Bcrypt
from functools import wraps

import re
import json

bcrypt = Bcrypt()

current_user = []


def login_required(f):
    """Check if user is logged in."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Wrap the function."""
        if len(current_user) == 0:
            return make_response(
                jsonify({
                    'Message': 'Unauthorized access. Please login!.'
                }), 401)

        return f(*args, **kwargs)

    return wrapper


# Namespaces
auth_namespace = api.namespace(
    'auth', description='Authentication Related Operation')

request_namespace = api.namespace(
    'users', description='Request Related Operation')

registration_model = api.model(
    'Registration', {
        "username":
        fields.String(
            required=True, description='Username', example="Joe_doe"),
        "email":
        fields.String(
            requires=True,
            description='email account',
            example="joe_doe@example.com"),
        "password":
        fields.String(
            requires=True,
            description="Your password account",
            example="U#76pJr3r")
    })

login_model = api.model(
    'Login', {
        "email":
        fields.String(
            requires=True,
            description='email account',
            example="joe_doe@example.com"),
        "password":
        fields.String(
            requires=True,
            description="Your password account",
            example="U#76pJr3r")
    })

Request_model = api.model(
    'Request', {
        "user_request":
        fields.String(
            requires=True, description='Request made', example="Plumbering"),
        "category":
        fields.String(
            requires=True,
            description="Is it maintenance or repair services",
            example="Repaire"),
        "location":
        fields.String(
            requires=True,
            description="Location",
            example="Westland st 12235 House: 345E")
    })

# User registration validation
email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@auth_namespace.route('/register')
class Registration(Resource):
    """Handles registration Routes."""

    @api.expect(registration_model)
    def post(self):
        """Register new user."""
        data = request.get_json()
        try:
            email = data['email']
            username = data['username']
            password = data['password']
        except KeyError:
            return {'Message': 'All input data required!'}, 400
        if len(email) > 5:
            if not re.match(email_regex, email):
                return {
                    'Message': '{} is not a valid email address'.format(email)
                }, 400
        else:
            return {
                'Message': 'Email address must be 6 characters or more'
            }, 411

        if [
                duplicate_email for duplicate_email in User.user_info
                if duplicate_email['email'] == email
        ]:
            return {'Message': 'Email already Exist'}, 406
        else:
            if len(password) <= 8:
                return {'Message': "Password must be greater than 8"}, 411
            else:
                user = User(username, email, password)
                return {
                    'Account': user.create_user(),
                    'Message': 'Successfully Registered'
                }, 201


@auth_namespace.route('/login')
class login(Resource):
    """Handle /login route."""

    @api.expect(login_model)
    def post(self):
        """Login a registered user."""
        data = request.get_json()
        try:
            email = data['email']
            password = data['password']
        except KeyError:
            return {'Message': 'Invalid, all input data required!'}, 400
        else:
            if [
                    user for user in User.user_info if user['email'] == email
                    and bcrypt.check_password_hash(user['password'], password)
            ]:
                global current_user
                current_user = [email]
                return {
                    "current_user": current_user,
                    'Message': 'Successfully logged in'
                }, 200
            else:
                return {"Message": "Incorrect Email or Password"}, 400


@auth_namespace.route('/logout')
class Logout(Resource):
    """Handle logout route."""

    def get(self):
        del current_user[:]
        return {"Message": "Successfully logged-out"}, 200


@request_namespace.route('/requests')
class RequestList(Resource):
    """Handle users/requests routes."""

    @login_required
    def get(self):
        """Handle [Endpoint] GET."""
        if len(CreateRequest.all_requests) == 0:
            return {"Message": 'No requesst found'}, 404
        else:
            return {"Requests": CreateRequest.all_requests}, 200

    @api.expect(Request_model)
    @login_required
    def post(self):
        """Handle [Endpoint] POST."""
        data = request.get_json()
        try:
            user_request = data['user_request']
            category = data['category']
            location = data['location']
        except KeyError:
            return {'Message': "All input data required"}, 400
        else:
            create = CreateRequest(user_request, category, location)
            create.save_request()
            return {"Message": "Request Successfully created"}, 201


@request_namespace.route('/requests/<int:requestId>')
class Request(Resource):
    """Handle  users/requests routes."""

    @api.expect(Request_model)
    @login_required
    def put(self, requestId):
        """Handle [endpoint] PUT."""
        request_update = [
            request_data for request_data in CreateRequest.all_requests
            if request_data['id'] == requestId
        ]
        if len(request_update) == 0:
            abort(404, "Not found!")

        data = request.get_json()

        try:
            request_update[0]['category'] = data['category']
            request_update[0]['user_request'] = data['user_request']
            request_update[0]['location'] = data['location']

        except KeyError:
            return {'Message': "All input data required!"}, 400
        else:
            return {"Message": "successfully updated"}, 201

    @login_required
    def get(self, requestId):
        """Get one request by ID."""
        one_request = [
            request_data for request_data in CreateRequest.all_requests
            if request_data['id'] == requestId
        ]
        if len(one_request) == 0:
            return {'Message': "Not found"}, 404
        else:
            return {'request': one_request}

    @login_required
    def delete(self, requestId):
        """Delete a request."""
        delete_request = [
            request_data for request_data in CreateRequest.all_requests
            if request_data['id'] == requestId
        ]
        if len(delete_request) == 0:
            return {'Message': 'Not found'}, 404
        else:
            CreateRequest.all_requests.remove(delete_request[0])
        return {
            "message": "Deleted {} successfully".format(delete_request[0])
        }, 200
