"""
Database models
"""
import uuid
import os
import phonenumbers

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_anonymous_user(self):
        """Create and return an anonymous user"""
        user = self.model(is_anonymous=True)
        user.save(using=self._db)
        return user

    def create_user_with_email_and_password(self, email, password=None, **extra_fields):
        """Create, save, and return a new user with an email and password"""
        if not email:
            raise ValueError("Email field is required")
        if not password:
            raise ValueError("Password field is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user_with_phone_number(self, phone_number, **extra_fields):
        """Create, save, and return a new user with a phone number"""
        if not phone_number:
            raise ValueError("Phone number field is required")
        user = self.model(
            phone_number=self.normalize_phone_number(phone_number), **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_user_with_facebook(self, facebook_id, **extra_fields):
        """Create, save, and return a new user with Facebook credentials"""
        if not facebook_id:
            raise ValueError("Facebook ID is required")
        user = self.model(**extra_fields)
        user.save(using=self._db)
        # Store the Facebook ID in the ProviderData
        ProviderData.objects.create(
            user=user, provider="facebook", provider_id=facebook_id
        )
        return user

    def create_user_with_apple(self, apple_id, **extra_fields):
        """Create, save, and return a new user with Apple credentials"""
        if not apple_id:
            raise ValueError("Apple ID is required")
        user = self.model(**extra_fields)
        user.save(using=self._db)
        # Store the Apple ID in the ProviderData
        ProviderData.objects.create(user=user, provider="apple", provider_id=apple_id)
        return user

    def normalize_phone_number(self, phone_number, default_region="PH"):
        """Normalize the phone number using the phonenumbers library"""
        try:
            parsed_number = phonenumbers.parse(phone_number, default_region)
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(
                    parsed_number, phonenumbers.PhoneNumberFormat.E164
                )
            else:
                raise ValueError(f"The phone number {phone_number} is not valid")
        except phonenumbers.NumberParseException:
            raise ValueError(f"The phone number {phone_number} is not valid")


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)  # To support anonymous users
    objects = UserManager()

    USERNAME_FIELD = "email"


class UserName(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first = models.CharField(max_length=255, default="")
    middle = models.CharField(max_length=255, blank=True, default="")
    last = models.CharField(max_length=255, default="")
    suffix = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.first} {self.middle} {self.last} {self.suffix}".strip()


class ProviderData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(
        max_length=50
    )  # e.g. 'facebook', 'apple', 'email', 'phone'
    provider_id = models.CharField(max_length=255, unique=True)
    metadata = JSONField(blank=True, null=True)  # Additional metadata if needed

    # Fields for data obtained from the provider
    name = models.OneToOneField(
        UserName, on_delete=models.SET_NULL, blank=True, null=True
    )
    photo_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email or self.user.phone_number} - {self.provider}"
