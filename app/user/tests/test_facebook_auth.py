"""
Test for the facebook auth api
"""
from unittest.mock import patch
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# ... [Your other imports]


CREATE_USER_FB_URL = reverse("user:create-facebook")


def mock_validate_token(*args, **kwargs):
    ret_val = "test@example.com"
    return ret_val


class PublicFacebookAuthTests(TestCase):
    """Test the Facebook auth API"""

    @patch("user.utils.requests.get")
    def test_valid_facebook_token_creates_user(self, mock_get):
        """Test that sending a valid Facebook token creates a user"""
        USER_EMAIL = "john.doe@example.com"
        mock_response = mock_get.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "user_id": "1234567890",
                "name": "John Doe",
                "email": USER_EMAIL,
            }
        }

        payload = {"facebook_id": "valid_facebook_token"}
        res = self.client.post(CREATE_USER_FB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=USER_EMAIL)

        print(f"user: {user}")
        self.assertIsNotNone(user)
        self.assertIn("email", res.data)  # Assuming you send back a token
        self.assertFalse(user.is_anonymous)

    @patch("user.utils.requests.get")
    def test_invalid_facebook_token(self, mock_get):
        """Test that an invalid Facebook token is rejected"""
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid token"}

        payload = {"facebook_id": "invalid_facebook_token"}
        res = self.client.post(CREATE_USER_FB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("user.utils.requests.get")
    def test_facebook_token_with_missing_email(self, mock_get):
        """Test handling a Facebook token with a missing email"""
        mock_response = mock_get.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "user_id": "1234567890",
                "name": "John Doe",
                # Email is intentionally missing here
            }
        }

        payload = {"facebook_id": "token_missing_email"}
        res = self.client.post(CREATE_USER_FB_URL, payload)
        print(f"resData: {res.data}")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("email", res.data)

    @patch(
        "user.serializers.user_with_facebook_serializer.validate_facebook_token",
        return_value=mock_validate_token,
    )
    def test_duplicate_user_handling(self, mock_validate_token):
        """Test handling a duplicate user sign up with Facebook"""
        payload = {"facebook_id": "mocked_facebook_token", "email": "test@example.com"}
        # First attempt
        res1 = self.client.post(CREATE_USER_FB_URL, payload)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", res1.data)
        # Duplicate attempt
        res2 = self.client.post(CREATE_USER_FB_URL, payload)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", res2.data)

    # ... Add more tests as needed ...
