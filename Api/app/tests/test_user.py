"""Test for User login and Registration."""
import unittest
import json
from app.models.user import User
from app import app


class UserApiTestCase(unittest.TestCase):
    """Testcase for login and registration."""

    def setUp(self):
        self.client = app.test_client
        self.user_details = {
            'username': 'Joe_test',
            'email': 'joe@email.com',
            'password': 'U#76pJr3r',
        }

    def tearDown(self):
        """Tear down all initialized variables."""
        del User.user_info[:]

    def test_registration(self):
        """Tests if user registration works correctly."""
        res = self.client().post(
            'api/v1/auth/register',
            content_type="application/json",
            data=json.dumps(self.user_details))
        # get the results in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'Successfully Registered')
        self.assertEqual(res.status_code, 201)

    def test_registration_with_short_password_provided(self):
        """Test api if user register with short password."""
        res = self.client().post(
            'api/v1/auth/register',
            data=json.dumps({
                'username': 'Joe',
                'email': 'Joe@example.com',
                'password': 'test'
            }),
            content_type="application/json")

        # get the result in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'Password must be greater than 8')

    def test_registration_with_less_data_provided(self):
        """Test api when user provide less input data required for registration."""
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

    def test_registration_with_short_email(self):
        """Test api when user register with invalid email syntax."""
        res = self.client().post(
            'api/v1/auth/register',
            data=json.dumps({
                'username': 'Joe',
                'email': 'a@a',
                'password': 'U#76pJr3r'
            }),
            content_type="application/json")

        # get the result in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'],
                         'Email address must be 6 characters or more')
        self.assertEqual(res.status_code, 411)

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
        self.assertEqual(results['Message'], 'Successfully logged in')

    def test_login_with_lesss_input_data(self):
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
                         'Invalid, all input data required!')
        self.assertEqual(login_res.status_code, 400)

    def test_login_password_mismatch(self):
        """Makes a post request to the api with wrong password and test login."""
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
        self.assertEqual(res['Message'], 'Incorrect Email or Password')

    def test_unregistered_user_login(self):
        """Test api response for unregistered user login."""
        none_exist = {"email": "fake@email.com", "password": 'aaabbbcccddd'}
        login_res = self.client().post(
            'api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(none_exist)
        result = json.loads(login_res.data)
        self.assertEqual(result['Message'], "Incorrect Email or Password")
        self.assertEqual(login_res.status_code, 400)

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
        self.assertEqual(result['Message'], 'Email already Exist')

    def test_logout_user(self):
        """Test api logout endpoint."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        logout_res = self.client().get('api/v1/auth/logout')
        self.assertEqual(logout_res.status, '200 OK')
