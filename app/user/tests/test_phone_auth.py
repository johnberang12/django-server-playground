"""
Test for the phone auth api
"""


"""
test_phone_auth.py

This file provides a commented outline for implementing phone authentication
in the future. When adding phone authentication, consider the following
implementation steps and corresponding tests.
"""


# from django.urls import reverse
# from django.test import TestCase
# from rest_framework import status
# from rest_framework.test import APIClient
# from core.models import User

# PHONE_REGISTER_URL = reverse('user:phone-register')
# TOKEN_URL = reverse('user:token_obtain_pair')

# class PublicPhoneAuthTests(TestCase):
#     """Test the phone authentication API (public)"""

#     def setUp(self):
#         self.client = APIClient()

#     def test_create_user_with_phone_number(self):
#         """Test that a user can register with a phone number"""
#         # Implementation: Allow users to register with a phone number.
#         # The system should send an OTP (One-Time Password) to the provided phone number.
#         # NOTE: Consider integrating with a service like Twilio for SMS OTP delivery.

#     def test_token_generation_for_phone_auth(self):
#         """Test token generation upon successful phone authentication"""
#         # Implementation: Upon successful phone number verification,
#         # the system should generate a token for the user.

#     def test_invalid_phone_number(self):
#         """Test error for an invalid phone number format"""
#         # Implementation: The system should validate the phone number format
#         # and return an error for invalid formats.

#     def test_existing_phone_number_registration(self):
#         """Test error for trying to register with an already registered phone number"""
#         # Implementation: The system should check if a phone number is already
#         # registered and return an error if a user tries to register with it again.

#     def test_invalid_otp_verification(self):
#         """Test error for invalid OTP or verification code"""
#         # Implementation: The system should validate the OTP sent to the user's phone.
#         # An invalid OTP should result in an error.

# class PrivatePhoneAuthTests(TestCase):
#     """Test the phone authentication API (private) for authenticated users"""

#     def setUp(self):
#         self.user = User.objects.create_user(phone_number='+1234567890')
#         self.client = APIClient()
#         self.client.force_authenticate(self.user)

#     # Tests for authenticated users will go here.
#     # For example, changing associated phone numbers, resending OTP, etc.

# """
# Additional considerations:
# 1. Rate Limiting: Implement rate limiting to prevent abuse of the phone auth endpoints.
# 2. Security: Ensure that OTPs expire after a certain duration or after a certain number of incorrect attempts.
# 3. Mocking: For testing purposes, consider mocking the external OTP service to avoid sending actual SMS messages.
# """
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import User
from django.contrib.auth import get_user_model


PHONE_REGISTER_URL = reverse("user:create-phone")
TOKEN_URL = reverse("authentication:phone-token-obtain-pair")


class PublicPhoneAuthTests(TestCase):
    """Test the phone authentication API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_phone_number(self):
        """Test that a user can register with a phone number"""
        payload = {"phone_number": "+639151234567"}
        res = self.client.post(PHONE_REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(phone_number=payload["phone_number"])

        self.assertIsNotNone(user)
        self.assertFalse(user.is_anonymous)

    # ... more tests to come


class PrivatePhoneAuthTests(TestCase):
    """Test the phone authentication API (private) for authenticated users"""

    def setUp(self):
        self.user = User.objects.create_user(phone_number="+639151234567")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # Tests for authenticated users will go here
