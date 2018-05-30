"""
Test for User login and Registration
"""
import unittest
import json
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
        self.user_details.clear()

    def register_user(self,
                      username='Test',
                      email='example@example.com',
                      password='test_password'):
        """Implied registration . A helper method"""
        user_details = {
            'email': email,
            'password': password,
            'Username': username,
        }
        return self.client().post('/api/v1/register', data=user_details)

    def login_user(self, email='user1234@gmail.com', password='testpassword'):
        """Implied login. A helper method"""
        self.user_data = {
            'email': email,
            'password': password,
        }
        return self.client().post('api/v1/login', data=self.user_data)

        def test_registration(self):
            """Tests if user registration works correctly"""
            res = self.client().post('/register', data=self.user_details)
            # get the results in json format
            result = json.loads(res)
            self.assertEqual(result['message'], 'Successfully Registered')
            self.assertEqual(res.status_code, 201)

    def test_registration_with_short_password_provided(self):
        """Makes a post request to the api with a password and tests if user
        will be registered"""
        res = self.client().post(
            'api/v1/register',
            data={
                'username': 'test',
                'email': 'example@example.com',
                'password': 'pasword',
            })
        # get the result in json format
        result = json.loads(res)
        self.assertEqual(result['message'], 'Password must be greater than 8')

    def test_login_password_mismatch(self):
        """Makes a post request to the api with wrong password and test login"""
        res = self.client().post(
            'api/v1/register',
            data={
                'Username': 'test',
                'email': 'example@example.com',
                'password': '123455678',
            })
        login_res = self.client().post(
            'api/v1/login',
            data={
                'email': 'test@example.com',
                'password': 'INVALID PASSWORD'
            })
        res = json.loads(login_res.data.decode())
        self.assertEqual(res['message'], 'Incorrect Email or Password')

    def test_user_login(self):
        """Test user login"""
        self.client().post('/v2/auth/register', data=self.user_data)
        login_res = self.client().post('/login', data=self.user_data)
        results = json.loads(login_res)
        self.assertEqual(results['message'], 'You have successfully logged in')

    def test_unregistered_user_login(self):
        none_exist = {"email": "asgh@googligoo.com", "password": 'bbbbasdghj'}
        login_res = self.client().post('api/v1/auth/login', data=none_exist)
        result = json.loads(login_res)
        self.assertEqual(result['message'], 'Incorrect Email or Password')

    def test_already_registered(self):
        """Test register a user who is already registered"""
        self.client().post('api/v1/auth/register', data=self.user_details)

        second_res = self.client().post(
            'api/v1/auth/register', data=self.user_details)
        result = json.loads(second_res)
        self.assertEqual(result['message'],
                         'User already exists. Please login')


if __name__ == '__main__':
    unittest.main()
