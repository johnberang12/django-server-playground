from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# TOKEN_URL = reverse(
#     "authentication:token_obtain_pair"
# )  # Adjust as needed based on your URL namespace


# def create_user(**params):
#     """Create and return a new user"""
#     return get_user_model().objects.create_user(**params)


# class PublicTokenApiTests(TestCase):
#     """Test the public features of the JWT token API"""

#     def setUp(self):
#         self.client = APIClient()

#     def test_create_token_for_valid_credentials(self):
#         """Test that a token is created for valid credentials"""
#         payload = {
#             "email": "test@example.com",
#             "password": "testpass123",
#         }
#         create_user(**payload)
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertIn("access", res.data)
#         self.assertIn("uid", res.data)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_create_token_invalid_credentials(self):
#         """Test that token is not created for invalid credentials"""
#         create_user(email="test@example.com", password="testpass123")
#         payload = {"email": "test@example.com", "password": "wrongpass"}
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn("access", res.data)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_create_token_no_user(self):
#         """Test that token is not created if user doesn't exist"""
#         payload = {"email": "test@example.com", "password": "testpass123"}
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn("access", res.data)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_create_token_missing_field(self):
#         """Test that email and password are required"""
#         res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
#         self.assertNotIn("access", res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
