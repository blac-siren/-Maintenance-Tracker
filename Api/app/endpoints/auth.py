"""Handle Authentication routes."""
from flask_restplus import Resource, Namespace, fields
from flask import request
from flask_bcrypt import Bcrypt
from psycopg2.extras import RealDictCursor
import json
import re

# local imports
from app.models.user import User
from app import manage

auth_namespace = Namespace(
    'auth', description='Authentication Related Operation.')

login_model = auth_namespace.model(
    'login_model', {
        'email':
        fields.String(
            required=True,
            description='your email accounts',
            example='john_doe@example.com'),
        'password':
        fields.String(
            required=True,
            description='Your secret password',
            example='U7r59enNp')
    })

registration_model = auth_namespace.inherit(
    'Registration', login_model, {
        'username':
        fields.String(
            required=True, description='Your username', example='john_doe')
    })

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@auth_namespace.route('/register')
class Registration(Resource):
    """Handles registration Routes."""

    @auth_namespace.expect(registration_model)
    def post(self):
        """Register new user."""
        data = request.get_json()
        try:
            email = data['email']
            username = data['username']
            password = data['password']
        except KeyError:
            return {'Message': 'All input data required!'}, 400
        if len(email) > 5 and not re.match(email_regex, email):
            return {
                'Message': '{} is not a valid email address'.format(email)
            }, 400

        emails = manage.all_email()
        if [email_db for email_db in emails if email_db['email'] == email]:
            return {'Message': 'Email already'}, 406

        if len(password) <= 8:
            return {'Message': "Password must be greater than 8"}, 411
        else:
            user = User(username, email, password)
            user.save_user()

            return {'Message': 'Successfully Registered'}, 201


@auth_namespace.route('/login')
@auth_namespace.doc(
    responses={
        200: 'Successfully login',
        400: 'Invalid input data provided',
        401: 'Unauthorized, Invalid credential'
    },
    security=None,
    body=login_model)
class Login(Resource):
    """login a registered user."""

    def post(self):
        """Handle POST request."""
        data = request.get_json()
        try:
            email = data['email']
            password = data['password']
            password_hash = manage.db_password_hash(email)
        except KeyError:
            return {'Message': 'Invalid credentials'}, 401
        else:
            if [
                    existing_emails for existing_emails in manage.all_email()
                    if existing_emails['email'] == email and Bcrypt()
                    .check_password_hash(password_hash['password'], password)
            ]:
                access_token = User.generate_token(email)

                return {
                    'Access token': access_token.decode(),
                    'Message': 'Successfully logged in!'
                }
            else:
                return {'Message': 'Incorrect email or password'}, 200
