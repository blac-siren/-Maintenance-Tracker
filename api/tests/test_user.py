"""
Test for User login and Registration
"""
import unittest
import json
from app.models.user import User
from app import app


class UserApiTestCase(unittest.TestCase):
    """
    Setup
    """

    def setUp(self):
        self.client = app.test_client
        self.user_details = {
            'username': 'Test',
            'email': 'example@example.com',
            'password': 'test_password',
        }

    def tearDown(self):
        """Tear down all initialized variables"""

        User.user_info.clear()

    def test_registration(self):
        """Tests if user registration works correctly"""
        res = self.client().post(
            'api/v1/register',
            content_type="application/json",
            data=json.dumps(self.user_details))
        # get the results in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'Successfully Registered')
        self.assertEqual(res.status_code, 201)

    def test_registration_with_short_password_provided(self):
        """Makes a post request to the api with a password and tests if user
        will be registered"""
        res = self.client().post(
            'api/v1/register',
            data=json.dumps({
                'username': 'Test',
                'email': 'example@example.com',
                'password': 'test'
            }),
            content_type="application/json")

        # get the result in json format
        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'Password must be greater than 8')

    def test_login_password_mismatch(self):
        """Makes a post request to the api with wrong password and test login"""
        res = self.client().post(
            'api/v1/register',
            content_type="application/json",
            data=json.dumps(self.user_details))

        login_res = self.client().post(
            'api/v1/login',
            data=json.dumps({
                'email': 'example@example.com',
                'password': "wrongpass"
            }),
            content_type="application/json")
        res = json.loads(login_res.data)
        self.assertEqual(res['Message'], 'Incorrect Email or Password ')

    def test_user_login(self):
        """Test user login"""
        self.client().post(
            'api/v1/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        results = json.loads(login_res.data)
        self.assertEqual(results['Message'], 'Successfully logged in')

    # def test_unregistered_user_login(self):
    #     none_exist = {"email": "asgh@googligoo.com", "password": 'bbbbasdghj'}
    #     login_res = self.client().post('api/v1/auth/login', data=none_exist)
    #     result = json.loads(login_res)
    #     self.assertEqual(result['message'], 'Incorrect Email or Password')

    def test_already_registered(self):
        """Test register a user who is already registered"""
        self.client().post(
            '/api/v1/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        second_res = self.client().post(
            '/api/v1/register',
            data=json.dumps(self.user_details),
            content_type="application/json")
        result = json.loads(second_res.data)
        self.assertEqual(result['message'], 'Email already Exist')


if __name__ == '__main__':
    unittest.main()
