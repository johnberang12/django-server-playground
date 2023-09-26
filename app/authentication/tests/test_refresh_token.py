from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# TOKEN_URL = reverse("authentication:token_obtain_pair")
# REFRESH_TOKEN_URL = reverse("authentication:token_refresh")


# def create_user(**params):
#     """Create and return a new user"""
#     return get_user_model().objects.create_user(**params)


# class RefreshTokenTests(TestCase):
#     """Test the token refresh features of the JWT token API"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user(
#             email="test@example.com",
#             password="testpass123",
#         )
#         self.client.force_authenticate(user=self.user)

#         # Obtain token
#         res = self.client.post(
#             TOKEN_URL,
#             {
#                 "email": "test@example.com",
#                 "password": "testpass123",
#             },
#         )
#         self.refresh_token = res.data["refresh"]

#     def test_refresh_token(self):
#         """Test that a new token is generated when using a valid refresh token"""
#         res = self.client.post(REFRESH_TOKEN_URL, {"refresh": self.refresh_token})

#         self.assertIn("access", res.data)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_refresh_token_invalid(self):
#         """Test that token is not refreshed for invalid refresh token"""
#         res = self.client.post(REFRESH_TOKEN_URL, {"refresh": "invalidtoken"})

#         self.assertNotIn("access", res.data)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
