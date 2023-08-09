import unittest
from unittest.mock import patch, Mock
import requests_mock
from app import app

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')  # Mock the requests.get function
    def test_index_route(self, mock_get):
        # Mock response from the posts service
        mock_response = Mock()
        mock_response.json.return_value = [{'_id': '123', 'title': 'Mock Post'}]
        mock_get.return_value = mock_response

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mock Post', response.data)

    @patch('app.requests.get')  # Mock the requests.get function
    def test_login(self, mock_get):
        # Mock response from the users service
        mock_response_user = Mock()
        mock_response_user.json.return_value = {'user': {'_id': 'example@gmail.com', 'password': 'hashed_password'}}
        mock_get.return_value = mock_response_user

        response = self.app.post('/login', data={'email': 'example@gmail.com', 'password': 'q1w2e3r4'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Blog', response.data)

    @patch('app.requests.post')  # Mock the requests.post function
    @patch('app.requests.get')   # Mock the requests.get function
    def test_register(self, mock_get, mock_post):
        # Mock response from the users service for checking existing user
        mock_response_user = Mock()
        mock_response_user.json.return_value = {'user': None}
        mock_get.return_value = mock_response_user

        # Mock response from the posts service for creating a new post
        mock_response_post = Mock()
        mock_response_post.json.return_value = {'post': '123'}
        mock_post.return_value = mock_response_post

        response = self.app.post('/register', data={'firstname': 'New', 'lastname': 'User', 'email': 'newuser@gmail.com', 'password': 'q1w2e3r4'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Blog', response.data)

    @patch('app.requests', autospec=True)
    def test_get_post(self, mock_requests):
        # Mock response from the posts service for getting a single post
        mock_response_get = {'post': {'_id': '123', 'title': 'Existing Post', 'content': 'Post Content', 'user_id':'example@gmail.com'}}
        mock_response_reviews = {'reviews': [{'_id': '1', 'post_id': '123', 'rating': {'rating': 5, 'color': 'orange'}, 'review': 'Great post!', 'user_id':'example@gmail.com'}]}
        mock_requests.get.side_effect = [MockResponse(mock_response_get), MockResponse(mock_response_reviews)]

        response = self.app.get('/posts/123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Existing Post', response.data)
        self.assertIn(b'Post Content', response.data)
        self.assertIn(b'Great post!', response.data)  # Check if the review comment is present

    @patch('app.requests', autospec=True)
    def test_add_post(self, mock_requests):
        # Mock response from the posts service for getting posts
        mock_response_get = [{'_id': '123', 'title': 'New Post', 'content': 'Content'}]
        mock_requests.get.return_value.json.return_value = mock_response_get

        # Mock response from the posts service for creating a new post
        mock_response_post = {'post': '123'}
        mock_requests.post.return_value.json.return_value = mock_response_post

        response = self.app.post('/posts', data={'title': 'New Post', 'content': 'Content'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Post', response.data)

    @patch('app.requests', autospec=True)
    def test_update_post(self, mock_requests):
        # Mock response from the posts service for updating a post
        mock_response_get = {'post': {'_id': '123', 'title': 'Updated Post', 'content': 'Updated Content', 'user_id':'example@gmail.com'}}
        mock_response_put = {'post': {'_id': '123', 'title': 'Updated Post', 'content': 'Updated Content', 'user_id':'example@gmail.com'}}
        mock_response_reviews = {'reviews': [{'_id': '1', 'post_id': '123', 'rating': {'rating': 5, 'color': 'orange'}, 'review': 'Great post!', 'user_id':'example@gmail.com'}]}
        mock_requests.get.side_effect = [MockResponse(mock_response_get), MockResponse(mock_response_reviews)]
        mock_requests.put.return_value.json.return_value = mock_response_put

        response = self.app.post('/posts/123/update', data={'title': 'Updated Post', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Post', response.data)
        self.assertIn(b'Updated Content', response.data)
        self.assertIn(b'Great post!', response.data)  # Check if the review comment is present

    @patch('app.requests', autospec=True)
    def test_delete_post(self, mock_requests):
        # Mock response from the posts service for getting a single post
        mock_response_get = [{'_id': '123', 'title': 'Existing Post', 'content': 'Existing Content', 'user_id':'example@gmail.com'}]
        mock_requests.get.return_value.json.return_value = mock_response_get

        # Mock response from the posts service for deleting a post
        mock_response_delete = {'deleted':1}
        mock_requests.delete.return_value.json.return_value = mock_response_delete

        response = self.app.post('/posts/123/delete')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Post to Delete', response.data)  # Check if the deleted post content is not present
        self.assertNotIn(b'Content to Delete', response.data)  # Check if the deleted post content is not present
        self.assertIn(b'Existing Post', response.data)  # Check if the existing post title is still present
        self.assertIn(b'Existing Content', response.data)  # Check if the existing post content is still present


if __name__ == '__main__':
    unittest.main()

