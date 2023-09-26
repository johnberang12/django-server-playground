import jwt
from datetime import datetime
from django.urls import reverse
from core.models import ProviderData
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model

CREATE_USER_APPLE_URL = reverse("user:create-apple")
KID = "W6WcOKB"
# MOCK_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.NHVaYe26MbtOYhSKkoKYdFVomg4i8ZJd8_-RU8VNbftc4TSMb4bXP3l3YlNWACwyXPGffz5aXHc6lty1Y2t4SWRqGteragsVdZufDn5BlnJl9pdR_kdVFUsra2rWKEofkZeIC4yWytE58sMIihvo9H1ScmmVwBcQP6XETqYd0aSHp1gOa9RdUPDvoXQ5oqygTqVtxaDr6wUFKrKItgBMzWIdNZ6y7O9E0DhEPTbE9rfBo6KTFsHAZnMg4k68CDp2woYIaXbmYTWcvbzIuHO7_37GT79XdIwkm95QJ7hYC9RiwrV7mesbY4PAahERJawntho0my942XheVLmGwLMBkQ"
mock_keys_response = {
    "keys": [
        {
            "kty": "RSA",
            "kid": KID,
            "use": "sig",
            "alg": "RS256",
            "n": "2Zc5d0-zkZ5AKmtYTvxHc3vRc41YfbklflxG9SWsg5qXUxvfgpktGAcxXLFAd9Uglzow9ezvmTGce5d3DhAYKwHAEPT9hbaMDj7DfmEwuNO8UahfnBkBXsCoUaL3QITF5_DAPsZroTqs7tkQQZ7qPkQXCSu2aosgOJmaoKQgwcOdjD0D49ne2B_dkxBcNCcJT9pTSWJ8NfGycjWAQsvC8CGstH8oKwhC5raDcc2IGXMOQC7Qr75d6J5Q24CePHj_JD7zjbwYy9KNH8wyr829eO_G4OEUW50FAN6HKtvjhJIguMl_1BLZ93z2KJyxExiNTZBUBQbbgCNBfzTv7JrxMw",
            "e": "AQAB",
        },
    ]
}


# Define the payload (claims)


# Your secret key (replace with your actual secret key)
secret_key = "YOUR_SECRET_KEY"


def mock_validate_apple_token(*args, **kwargs):
    return "test.apple@example.com"


class PublicAppleAuthTests(APITestCase):
    """Test the Apple auth API"""

    # ... other test methods ...

    @patch("user.utils.jwt.decode")
    def test_valid_apple_token_creates_user(self, mock_jwt_decode):
        """Test that sending a valid Apple token creates a user"""
        USER_EMAIL = "john.apple@example.com"
        # Mocking the jwt.decode function to return a predefined payload
        mock_jwt_decode.return_value = {
            "sub": "1234567890",
            "name": "John Doe",
            "email": USER_EMAIL,
            "admin": True,
            "iat": 1516239022,
        }
        payload = {
            "sub": "1234567890",
            "name": "John Doe",
            "email": USER_EMAIL,
            "admin": True,
            "iat": int(datetime.utcnow().timestamp()),
        }
        # Define the header with your custom "kid"
        header = {
            "kid": KID,
            "alg": "HS256",  # Use the appropriate algorithm
        }
        # Create the JWT token
        MOCK_JWT = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)

        payload = {"apple_id": MOCK_JWT}
        res = self.client.post(CREATE_USER_APPLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # user_exists = (
        #     get_user_model().objects.filter(email="john.apple@example.com").exists()
        # )
        user = get_user_model().objects.get(email=USER_EMAIL)
        self.assertFalse(user.is_anonymous)

        providerdata_exists = ProviderData.objects.filter(
            user__email=USER_EMAIL, provider="apple"
        ).exists()

        self.assertTrue(providerdata_exists)

    @patch("user.utils.requests.get")
    def test_invalid_apple_token(self, mock_get):
        """Test that an invalid Apple token is rejected"""
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid token"}

        payload = {"apple_id": "invalid_apple_token"}
        res = self.client.post(CREATE_USER_APPLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # @patch("user.utils.requests.get")
    # def test_apple_token_with_missing_email(self, mock_get):
    #     """Test handling an Apple token with a missing email"""
    #     mock_response = mock_get.return_value
    #     mock_response.status_code = 200
    #     mock_response.json.return_value = {
    #         "error": "invalid_request",
    #         "error_description": "Email is missing in Apple token.",
    #     }  # Empty response (missing email)

    #     payload = {"apple_id": "token_missing_email"}
    #     res = self.client.post(CREATE_USER_APPLE_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("Email is missing in Apple token.", res.data["detail"])

    @patch(
        "user.serializers.user_with_apple_serializer.validate_apple_token",
        return_value=mock_validate_apple_token,
    )
    def test_duplicate_user_handling(self, mock_validate_token):
        """Test handling a duplicate user sign up with Apple"""
        payload1 = {"apple_id": "mocked_apple_token", "email": "test.apple@example.com"}
        # First attempt
        res1 = self.client.post(CREATE_USER_APPLE_URL, payload1)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", res1.data)
        # Duplicate attempt
        payload2 = {
            "apple_id": "mocked_apple_token",
        }
        res2 = self.client.post(CREATE_USER_APPLE_URL, payload2)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", res2.data)

    # ... Add more tests as needed ...
