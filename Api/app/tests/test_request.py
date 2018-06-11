"""Module for request testcase."""
import unittest
import json

# local imports
from app.api import create_app
from app.DB.table_db import create_tables, drop_tables
from app.api import db


class RequestTestCase(unittest.TestCase):
    """This class represents the request test case."""

    def setUp(self):
        """Set up the data."""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.request = {
            "user_request": "Plumbering",
            "location": "Hurligham",
            "category": "Maintenance",
        }
        self.user_details = {
            'username': 'Joetest',
            'email': 'joe@email.com',
            'password': 'U#76pJr3r',
        }
        self.admin_details = {
            'username': 'Joetest',
            'email': 'joe@email.com',
            'password': 'U#76pJr3r',
            'admin': True
        }

    def tearDown(self):
        """Teardown all initialized data."""
        drop_tables(db)
        create_tables(db)

    def test_make_request_without_token_access(self):
        """Test create request (POST request) without token access."""
        res = self.client().post(
            'api/v1/users/requests',
            data=json.dumps(self.request),
            content_type='application/json')

        result = json.loads(res.data)
        self.assertEqual(result['Message'],
                         "Unauthorized, access token required!")
        self.assertEqual(res.status_code, 401)

    def test_create_request(self):
        """Test create request (POST request) with token."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type='application/json')

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        res = self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request),
            headers=dict(access_token=access_token))

        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'Request Successfully created')
        self.assertEqual(res.status_code, 201)

    def test_api_fetch_all_request(self):
        """Test API fetch all request (GET request)."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request),
            headers=dict(access_token=access_token))

        res = self.client().get(
            '/api/v1/users/requests',
            content_type="application/json",
            headers=dict(access_token=access_token))
        self.assertEqual(res.status_code, 200)

    def test_api_when_no_request_found(self):
        """Test Api when no request found."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type='application/json')

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']

        res1 = self.client().get(
            '/api/v1/users/requests',
            content_type="application/json",
            headers=dict(access_token=access_token))
        self.assertEqual(res1.status_code, 404)

    def test_request_can_be_edited(self):
        """Test API can edit an existing  request. (POST request)."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request),
            headers=dict(access_token=access_token))

        edit_res = self.client().put(
            'api/v1/users/requests/1',
            data=json.dumps({
                "user_request": "gardening",
                "location": "Pangani",
                "category": "maintenance"
            }),
            content_type='application/json',
            headers=dict(access_token=access_token))
        self.assertEqual(edit_res.status_code, 201)
        reslt = json.loads(edit_res.data)
        self.assertIn(reslt['Message'], 'successfully updated')

    def test_updating_with_less_input_data(self):
        """Test API when edit an existing  request and omit a input data. (POST request)."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request),
            headers=dict(access_token=access_token))

        edit_res = self.client().put(
            'api/v1/users/requests/1',
            data=json.dumps({
                "user_request": "gardening",
                "location": "Pangani"
            }),
            content_type='application/json',
            headers=dict(access_token=access_token))

        res = json.loads(edit_res.data)
        self.assertIn(res['Message'], 'All input data required!')

    def test_request_not_found_by_id(self):
        """Test Api response when no request. (GET request)."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request),
            headers=dict(access_token=access_token))

        res = self.client().get(
            '/api/v1/users/requests/10',
            headers=dict(access_token=access_token))
        self.assertEqual(res.status_code, 404)

    def test_edit_no_found_request(self):
        """Test API when edit not found request."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        edit_res = self.client().put(
            'api/v1/users/requests/10',
            data=json.dumps({
                "user_request": "gardening",
                "location": "Pangani",
                "category": "maintenance"
            }),
            content_type='application/json',
            headers=dict(access_token=access_token))
        self.assertEqual(edit_res.status_code, 404)
        reslt = json.loads(edit_res.data)
        self.assertIn(reslt['Message'], 'No request found!')

    def test_delete_request_by_id(self):
        """Test Api delete response."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        login_res = self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request),
            headers=dict(access_token=access_token))

        res = self.client().post(
            '/api/v1/users/requests',
            data=json.dumps(self.request),
            content_type='application/json',
            headers=dict(access_token=access_token))

        self.assertEqual(res.status_code, 201)
        del_res = self.client().delete(
            '/api/v1/users/requests/1',
            headers=dict(access_token=access_token))
        self.assertEqual(del_res.status_code, 200)

        # admin endpoints
    def test_unathorized_admin(self):
        res= self.client().get(
        'api/v1/requests/',
        content_type="application/json")
        self.assertEqual(res.status_code, 401)

    def test_unauthorized_approved_request(self):
        self.client().post(
        'api/v1/auth/register',
        data=json.dumps(self.admin_details),
        content_type="application/json")

        login_res = self.client().post(
        'api/v1/auth/login',
        data=json.dumps(self.admin_details),
        content_type="application/json")

        access_token = json.loads(login_res.data.decode())['Access token']
        self.client().post(
        '/api/v1/users/requests',
        content_type="application/json",
        data=json.dumps(self.request),
        headers=dict(access_token=access_token))

        edit_res = self.client().put(
        'api/v1/requests/1/approve',
        data=json.dumps({
        "status": "approve"
        }),
        content_type='application/json',
        headers=dict(access_token=access_token))

        self.assertEqual(edit_res.status_code, 403)




