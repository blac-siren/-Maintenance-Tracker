"""Testcase for Request."""

import unittest
import json

from app import app


class RequestTestCase(unittest.TestCase):
    """This class represents the request test case"""

    def setUp(self):
        """sets up the data."""
        self.client = app.test_client
        self.request = {
            "requested": "Plumbering",
            "location": "Hurligham",
            "category": "Maintenance"
        }

    def tearDown(self):
        """teardown all initialized data."""
        self.request.clear()

    def test_make_request(self):
        """Test create request (POST request)"""
        res = self.client().post(
            'api/v1/users/requests',
            data=json.dumps({
                "category": "maintenance",
                "location": "Nairobi",
                "req": "plumbering"
            }),
            content_type='application/json')
        print('####################', res)
        # result = json.loads(res)
        # self.assertEqual(result['message'], 'Succesfully created')
        self.assertEqual(res.status_code, 201)

    # def test_api_fetch_all_request(self):
    #     """Test API fetch all request (GET request)."""
    #     res = self.client().post('/api/v1/users/requests', data=self.request)
    #     self.assertEqual(res['message'], 'Succesfully created')
    #     res = self.client().get('/api/v1/users/requests')
    #     self.assertEqual(res.status_code, 200)

    # def test_api_can_get_request_by_id(self):
    #     """Test API can get a single request using id."""
    #     res = self.client().post('/api/v1/users/requests', data=self.request)
    #     self.assertEqual(res.status_code, 201)
    #     result = self.client().get('/api/v1/users/requests/1')
    #     self.assertEqual(result.status_code, 200)

    # def test_request_can_be_edited(self):
    #     """Test API can edit an existing  request. (POST request)."""
    #     res = self.client().post('/api/v1/users/requests', data=self.request)
    #     self.assertEqual(res.status_code, 201)
    #     edit_res = self.client().put(
    #         'api/v1/requests/1',
    #         data={
    #             "request": "gardening",
    #             "location": "Pangani"
    #         })
    #     self.assertEqual(edit_res.status_code, 201)
    #     results = self.client().get('/api/v1/requests/1')
    #     self.assertIn('{"request":"gardening", "location": "Pangani"}',
    #                   str(results.data))

    # def test_request_not_found_by_id(self):
    #     """Test Api response when no request. (GET request)."""
    #     res = self.client().get('/api/v1/users/requests/2t')
    #     self.assertEqual(res.status_code, 404)

    # def test_long_sentence_in_make_request(self):
    #     """Test API long sentence."""
    #     res = self.client().post('/api/v1/users/requests', data='fooo' * 100)
    #     result = json.loads(res)
    #     self.assertEqual(result['message'], "Too long")
    #     self.assertEqual(res.status_code, 411)

    # def test_edit_no_found_request(self):
    #     """Test API when edit not found request"""
    #     res = self.client().put(
    #         'api/v1/requests/r3',
    #         data={
    #             'request': 'grading',
    #             'location': 'pangami'
    #         })
    #     result = json.loads(res)
    #     self.assertEqual(result["message"], "Request Not Found!")
    #     self.assertEqual(res.status_code, 404)

    # def test_delete_request_by_id(self):
    #     """Test Api delete response."""
    #     res = self.client().post('/api/v1/users/requests', data=self.request)
    #     self.assertEqual(res.status_code, 201)
    #     del_res = self.client().delete('/api/v1/requests/1')
    #     result = json.loads(res)
    #     self.assertEqual(result['message'], "Successfully deleted")
    #     self.assertEqual(del_res.status_code, 200)

    # def test_delete_request_not_found(self):
    #     res = self.client().delete('api/v1/users/3e')
    #     result = json.loads(res)
    #     self.assertEqual(result['message'], 'Not found!')
    #     self.assertEqual(res.status_code, 404)


# if __name__ == "__main__":
#     unittest.main()