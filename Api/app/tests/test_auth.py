"""Module for Authentication endpoint tests."""
from app.tests.base import BaseApiTestcase
import json


class TestAuthEndpoints(BaseApiTestcase):
    """Class that handle authentication testcase."""

    # test registration
    def test_registration(self):
        """Test user registration."""
        response = self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type='application/json')

        # get the result in json format
        result = json.loads(response.data)
        self.assertEqual(result['Message'], 'Successfully Registered')
        self.assertEqual(response.status_code, 201)

    def test_register_with_short_password(self):
        """Test short password."""
        response = self.client().post(
            'api/v1/auth/register',
            data=json.dumps({
                'username': 'Joe',
                'email': 'Joe@example.com',
                'password': 'test'
            }),
            content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(result['Message'],
                         'Password must be atleast 8 characters')

    def test_registration_with_invalid_email_syntax(self):
        """Test api when user register with invalid email syntax."""
        res = self.client().post(
            'api/v1/auth/register',
            data=json.dumps({
                'username': 'Joe',
                'email': 'apple.com',
                'password': 'U#76pJr3r'
            }),
            content_type="application/json")

        # get the result in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'],
                         'apple.com is not a valid email address')
        self.assertEqual(res.status_code, 400)

    def test_registration_with_less_data_provided(self):
        """Test less input data required for registration."""
        res = self.client().post(
            'api/v1/auth/register',
            data=json.dumps({
                'username': 'Joe',
                'email': 'Joe@example.com',
            }),
            content_type="application/json")

        # get the result in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'All input data required!')
        self.assertEqual(res.status_code, 400)

    def test_already_registered(self):
        """Test email already registered."""
        self.client().post(
            '/api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        second_res = self.client().post(
            '/api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        result = json.loads(second_res.data)
        self.assertEqual(result['Message'], 'Email already exist')

    # test login
    def test_user_login(self):
        """Test user login."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        results = json.loads(login_res.data)
        self.assertEqual(results['Message'], 'Successfully logged in!')

    def test_login_with_less_input_data(self):
        """Test user login."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps({
                "email": "joedoe@email.com"
            }),
            content_type="application/json")

        results = json.loads(login_res.data)
        self.assertEqual(results['Message'],
                         'Unauthorized, Invalid credentials!')
        self.assertEqual(login_res.status_code, 400)

    def test_mismatch_password_login(self):
        """Test a post login request to the api with wrong password."""
        res = self.client().post(
            'api/v1/auth/register',
            content_type="application/json",
            data=json.dumps(self.user_details))

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps({
                'email': 'joe@example.com',
                'password': "wrongpass"
            }),
            content_type="application/json")
        res = json.loads(login_res.data)
        self.assertEqual(res['Message'], 'Incorrect email or password')

    def test_unregistered_user_login(self):
        """Test api response for unregistered user login."""
        none_exist = {"email": "fake@email.com", "password": 'aaabbbcccddd'}
        login_res = self.client().post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(none_exist))

        result = json.loads(login_res.data)
        self.assertEqual(result['Message'], "Incorrect email or password")
        self.assertEqual(login_res.status_code, 401)
