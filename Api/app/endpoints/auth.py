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
        if len(email) > 5:
            if not re.match(email_regex, email):
                return {
                    'Message': '{} is not a valid email address'.format(email)
                }, 400
        else:
            return {
                'Message': 'Email address must be 6 characters or more'
            }, 411
        conn = manage.connectTODB()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT email FROM users""")
        print(json.dumps(cur.fetchall(), indent=2))
        # return json.dumps(cur.fetchall(), indent=2)

        emails = json.dumps(cur.fetchall(), indent=2)
        conn.close()

        print(type(emails))
        print(emails)
        print('sssssssssssssssssss')
        if [email_db for email_db in emails if email_db['email'] == email]:
            return {'Message': 'Email already'}, 406

        if len(password) <= 8:
            return {'Message': "Password must be greater than 8"}, 411
        else:
            user = User(username, email, password)
            user.save_user()

            return {'Message': 'Successfully Registered'}, 201
