"""Handle Authentication routes."""
from flask_restplus import Resource, Namespace, fields
from flask import request
from flask_bcrypt import Bcrypt
from psycopg2.extras import RealDictCursor
import json
import re

# local imports
from app.models.user import User
from app.DB import manage

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
pattern = re.compile(r"(^[A-Za-z]+$)")


@auth_namespace.route('/register')
class Registration(Resource):
    """Handles registration Routes."""

    @auth_namespace.expect(registration_model)
    def post(self):
        """Register new user."""
        data = request.get_json()
        emails = manage.get_all_emails()
        try:
            email = data['email']
            username = data['username']
            password = data['password']
        except KeyError:
            return {'Message': 'All input data required!'}, 400

        if not re.match(pattern, username):
            return {
                'Status': 'Error',
                'Message': '{} is invalid username '.format(username)
            }, 400

        if [email_db for email_db in emails if email_db['email'] == email]:
            return {'Message': 'Ooops! Email already exist'}, 406

        # checks email syntax
        if not re.match(email_regex, email):
            return {
                'Status': 'Error',
                'Message':
                'Ooops! {} is not a valid email address'.format(email)
            }, 400
        if len(password) <= 8:
            return {'Message': "Password must be atleast 8 characters"}, 411
        else:
            user = User(username, email, password)
            user.save_user()

            return {'Message': 'Your Successfully Registered'}, 201


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
            password_hash = manage.get_password_hash(email)
        except KeyError:
            return {'Message': 'Unauthorized, Invalid credentials!'}, 400
        else:
            if [
                    existing_emails
                    for existing_emails in manage.get_all_emails()
                    if existing_emails['email'] == email and Bcrypt()
                    .check_password_hash(password_hash['password'], password)
            ]:
                access_token = User.generate_token(email)
                confirm = manage.confirm_admin(email)
                if len(confirm) == 0:
                    return {
                        'Access_token': access_token.decode(),
                        'Message': 'Successfully logged in!'
                    }, 200
                else:
                    return {
                        'Access_token': access_token.decode(),
                        "Message": "Welcome Admin"
                    }, 200
            else:
                return {'Message': 'Incorrect email or password'}, 401
