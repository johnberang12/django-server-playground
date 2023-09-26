"""
Test for the anonymous auth api
"""

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import User

CREATE_ANONYMOUS_USER_URL = reverse("user:create-anonymous")
ME_URL = reverse("user:me")


class AnonymousUserApiTests(TestCase):
    """Test the anonymous user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_anonymous_user_success(self):
        """Test creating an anonymous user is successful."""
        res = self.client.post(CREATE_ANONYMOUS_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=res.data["uid"])
        self.assertTrue(user.is_anonymous)
        self.assertIsNone(user.email)
        self.assertIsNone(user.phone_number)

    def test_anonymous_user_no_provider_data(self):
        """Test that an anonymous user has no associated provider data."""
        res = self.client.post(CREATE_ANONYMOUS_USER_URL)

        user = User.objects.get(pk=res.data["uid"])

        self.assertFalse(user.providerdata_set.exists())

    def test_multiple_anonymous_users_distinct(self):
        """Test creating multiple anonymous users results in distinct users."""
        self.client.post(CREATE_ANONYMOUS_USER_URL)
        self.client.post(CREATE_ANONYMOUS_USER_URL)

        users = User.objects.filter(is_anonymous=True)
        self.assertEqual(users.count(), 2)

    def test_anonymous_user_cannot_access_user_details(self):
        """Test that an anonymous user can't access the user/me endpoint."""

        # Create an anonymous user.
        res_create_anonymous = self.client.post(CREATE_ANONYMOUS_USER_URL)
        anonymous_user = User.objects.get(pk=res_create_anonymous.data["uid"])

        # Simulate that anonymous user trying to access the ME_URL.
        # You might need some way to authenticate as this anonymous user, like a token,
        # depending on how your system is set up.
        # For now, I'll use force_authenticate method. If your system uses a different method, adjust accordingly.
        self.client.force_authenticate(user=anonymous_user)

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
