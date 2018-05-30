import unittest
import json

from app.api.app.__init__ import app


class RequestTestCase(unittest.TestCase):
    """This class represents the request test case"""

    def setUp(self):
        """sets up the data."""
        self.client = app.test_client
        self.request = {"request": "Plumbering", "location": "Hurligham"}

    def tearDown(self):
        """teardown all initialized data."""
        self.request.clear()

    def test_make_request(self):
        """Test create request (POST request)"""
        res = self.client().post('/api/v1/users/requests', data=self.request)
        result = json.loads(res)
        self.assertEqual(result['message'], 'Succesfully created')

    def test_api_fetch_all_request(self):
        """Test API fetch all request (GET request)."""
        res = self.client().post('/api/v1/users/requests', data=self.request)
        self.assertEqual(res['message'], 'Succesfully created')
        res = self.client().get('/api/v1/users/requests')
        self.assertEqual(res.status_code, 200)

    def test_api_can_get_request_by_id(self):
        """Test API can get a single request using id."""
        res = self.client().post('/api/v1/users/requests', data=self.request)
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/api/v1/users/requests/1')
        self.assertEqual(result.status_code, 200)

    def test_request_can_be_edited(self):
        """Test API can edit an existing  request. (PUT request)."""
        res = self.client().post('/api/v1/users/requests', data=self.request)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            'api/v1/requests/1',
            data={
                "request": "gardening",
                "location": "Pangani"
            })
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/api/v1/requests/1')
        self.assertIn('{"request":"gardening", "location": "Pangani"}',
                      str(results.data))

    def test_request_not_found_by_id(self):
        """Test Api responds when no request. (GET request)."""
        res = self.client().get('/api/v1/users/requests/2t')
        self.assertEqual(res.status_code, 404)

    def test_long_sentence_in_make_request(self):
        """Test API long sentence."""
        res = self.client().post('/api/v1/users/requests', data='fooo' * 100)
        result = json.loads(res)
        self.assertEqual(result['message'], "Too long")
        self.assertEqual(res.status_code, 411)

    def test_edit_no_found_request(self):
        """Test API when edit not found request"""
        res = self.client().put(
            'api/v1/requests/r3',
            data={
                'request': 'grading',
                'location': 'pangami'
            })
        result = json.loads(res)
        self.assertEqual(result["message"], "Request Not Found!")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()