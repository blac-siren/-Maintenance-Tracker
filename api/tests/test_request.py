import unittest
import json

class RequestTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """sets up the data."""
        self.client = self.app.test_client
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
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/users/requests')
        self.assertEqual(res.status_code, 200)

    def test_api_can_get_request_by_id(self):
        """Test API can get a single request using id."""
        res = self.client().post('/api/v1/users/requests', data=self.request)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res)
        result = self.client().get('/bucketlists/{}'.format(
            result_in_json['id']))
        self.assertEqual(result.status_code, 200)


    def test_request_can_be_edited(self):
        """Test API can edit an existing  request. (PUT request)"""
        res = self.client().post('/api/v1/users/requests', data=self.request)
        self.assertEqual(rv.status_code, 201)
        res = self.client().put(
            'api/v1/requests/1',
            data={"request":"gardening", "location": "Pangani"})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/api/v1/requests/1')
        self.assertIn('{"request":"gardening", "location": "Pangani"}', str(results.data))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()