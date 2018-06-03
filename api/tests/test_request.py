"""Testcase for Request."""

import unittest
import json
from app.models.request import CreateRequest
from app.models.user import User
from app import app


class RequestTestCase(unittest.TestCase):
    """This class represents the request test case"""

    def setUp(self):
        """sets up the data."""
        self.client = app.test_client
        self.request = {
            "user_request": "Plumbering",
            "location": "Hurligham",
            "category": "Maintenance"
        }
        self.user_details = {
            'email': 'joe@email.com',
            'password': 'U#76pJr3r',
            'username': 'Joe_test'
        }

    def tearDown(self):
        """teardown all initialized data."""
        del CreateRequest.all_requests[:]
        del User.user_info[:]

    def test_make_request(self):
        """Test create request (POST request)"""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res = self.client().post(
            'api/v1/users/requests',
            data=json.dumps(self.request),
            content_type='application/json')

        result = json.loads(res.data)
        self.assertEqual(result['Message'], "Request Successfully created")
        self.assertEqual(res.status_code, 201)

    def test_api_fetch_all_request(self):
        """Test API fetch all request (GET request)."""

        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res = self.client().post(
            '/api/v1/users/requests',
            content_type="application/json",
            data=json.dumps(self.request))
        result = json.loads(res.data)
        self.assertEqual(result['Message'], 'Request Successfully created')

        res1 = self.client().get(
            '/api/v1/users/requests', content_type="application/json")
        self.assertEqual(res1.status_code, 200)

    def test_api_when_no_request_found(self):
        """Test Api when no request found."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res1 = self.client().get(
            '/api/v1/users/requests', content_type="application/json")
        self.assertEqual(res1.status_code, 404)

    def test_api_can_get_request_by_id(self):
        """Test API can get a single request using id."""

        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")
        res = self.client().post(
            '/api/v1/users/requests',
            content_type='application/json',
            data=json.dumps(self.request))
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/api/v1/users/requests/1')
        self.assertEqual(result.status_code, 200)

    def test_request_can_be_edited(self):
        """Test API can edit an existing  request. (POST request)."""

        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res = self.client().post(
            '/api/v1/users/requests',
            data=json.dumps(self.request),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)

        edit_res = self.client().put(
            'api/v1/users/requests/1',
            data=json.dumps({
                "user_request": "gardening",
                "location": "Pangani",
                "category": "maintenance"
            }),
            content_type='application/json')
        self.assertEqual(edit_res.status_code, 201)
        reslt = json.loads(edit_res.data)
        self.assertIn(reslt['Message'], 'successfully updated')

    def test_updating_with_less_input_data(self):
        """Test API when edit an existing  request and omit a input data. (POST request)."""

        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res = self.client().post(
            '/api/v1/users/requests',
            data=json.dumps(self.request),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)

        edit_res = self.client().put(
            'api/v1/users/requests/1',
            data=json.dumps({
                "user_request": "gardening",
                "category": "maintenance"
            }),
            content_type='application/json')
        self.assertEqual(edit_res.status_code, 400)
        reslt = json.loads(edit_res.data)
        self.assertIn(reslt['Message'], 'All input data required!')

    def test_request_not_found_by_id(self):
        """Test Api response when no request. (GET request)."""
        res = self.client().get('/api/v1/users/requests/2t')
        self.assertEqual(res.status_code, 404)

    def test_edit_no_found_request(self):
        """Test API when edit not found request"""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res = self.client().put(
            'api/v1/users/requests/44',
            data=json.dumps({
                'user_request': 'grading',
                'location': 'pangami',
                "category": "maintenance"
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_delete_request_by_id(self):
        """Test Api delete response."""
        self.client().post(
            'api/v1/auth/register',
            data=json.dumps(self.user_details),
            content_type="application/json")

        self.client().post(
            'api/v1/auth/login',
            data=json.dumps(self.user_details),
            content_type="application/json")

        res = self.client().post(
            '/api/v1/users/requests',
            data=json.dumps(self.request),
            content_type='application/json')

        self.assertEqual(res.status_code, 201)
        del_res = self.client().delete('/api/v1/users/requests/1')
        self.assertEqual(del_res.status_code, 200)

    def test_delete_request_not_found(self):
        res = self.client().delete('api/v1/users/requests/3e')
        self.assertEqual(res.status_code, 404)
