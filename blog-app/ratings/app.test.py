import unittest
import json
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.collection')
    def test_add_rating(self, mock_collection):
        review_id = '12345'
        rating = 4

        inserted_rating = MagicMock(inserted_id='60458fb603c395f9a81c9f4a')
        mock_collection.insert_one.return_value = inserted_rating

        response = self.app.post(f'/review/{review_id}/rating/{rating}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertIn('rating_id', data)

    @patch('app.collection')
    def test_get_rating(self, mock_collection):
        review_id = '12345'
        mock_collection.find_one.return_value = {'rating': 4}

        response = self.app.get(f'/review/{review_id}/rating')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['rating'], 4)
        self.assertEqual(data['color'], 'orange')

    @patch('app.collection')
    def test_get_nonexistent_rating(self, mock_collection):
        review_id = '12345'
        mock_collection.find_one.return_value = None

        response = self.app.get(f'/review/{review_id}/rating')

        self.assertEqual(response.status_code, 404)

    @patch('app.collection')
    def test_update_rating(self, mock_collection):
        review_id = '12345'
        rating = 5
        mock_collection.find_one_and_update.return_value = {'rating': 5}

        response = self.app.put(f'/review/{review_id}/rating/{rating}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['rating'], 5)

    @patch('app.collection')
    def test_update_nonexistent_rating(self, mock_collection):
        review_id = '12345'
        rating = 5
        mock_collection.find_one_and_update.return_value = None

        response = self.app.put(f'/review/{review_id}/rating/{rating}')

        self.assertEqual(response.status_code, 404)

    @patch('app.collection')
    def test_delete_rating(self, mock_collection):
        review_id = '12345'
        mock_result = MagicMock(deleted_count=1)
        mock_collection.delete_one.return_value = mock_result

        response = self.app.delete(f'/review/{review_id}/rating')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 1)

if __name__ == '__main__':
    unittest.main()

