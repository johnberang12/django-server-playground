"""
Test for models
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_anonymous_user_successful(self):
        """Test creating an anonymous user is successful."""
        user = get_user_model().objects.create_anonymous_user()
        self.assertTrue(user.is_anonymous)
        self.assertIsNone(user.email)
        self.assertIsNone(user.phone_number)

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user_with_email_and_password(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user_with_email_and_password(
                email, "sample123"
            )
            self.assertEqual(user.email, expected)

    def test_create_user_with_phone_number_successful(self):
        """Test creating a user with a phone number is successful."""
        phone_number = "+639155123456"
        user = get_user_model().objects.create_user_with_phone_number(phone_number)

        self.assertEqual(user.phone_number, phone_number)

    def test_create_user_with_facebook_successful(self):
        """Test creating a user with Facebook credentials is successful."""
        facebook_id = "1234567890"
        user = get_user_model().objects.create_user_with_facebook(facebook_id)

        provider_data = models.ProviderData.objects.get(user=user, provider="facebook")
        self.assertEqual(provider_data.provider_id, facebook_id)

    def test_create_user_with_apple_successful(self):
        """Test creating a user with Apple credentials is successful."""
        apple_id = "A1B2C3D4E5"
        user = get_user_model().objects.create_user_with_apple(apple_id)

        provider_data = models.ProviderData.objects.get(user=user, provider="apple")
        self.assertEqual(provider_data.provider_id, apple_id)
