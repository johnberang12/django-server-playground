from user.serializers.base_user_serializer import BaseUserSerializer
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class UserWithEmailSerializer(BaseUserSerializer):
    """Serializer for creating a user with an email and password."""

    class Meta(BaseUserSerializer.Meta):
        # We're inheriting fields from the BaseUserSerializer, so no need to redefine them
        extra_kwargs = {
            **BaseUserSerializer.Meta.extra_kwargs,
            "email": {"required": True},
            "phone_number": {"write_only": True, "required": False, "default": None},
            "password": {"write_only": True, "min_length": 5, "required": True},
        }

    def validate_email(self, email):
        # Check if email format is valid
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError(
                {
                    "detail": "The provided email address doesn't appear to be in a proper format. Please double-check and enter a valid email address.",
                    "code": "invalid-email",
                }
            )

        # Check if the email already exists
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    "detail": "The email address you provided is already in use. Please try another email or sign in.",
                    "code": "email-already-in-use",
                }
            )
        return email

    def validate_password(self, password):
        # Basic check for password strength (e.g., length). For more comprehensive checks, consider using `django-password-validation`.
        if len(password) < 8:  # Adjust this length based on your needs
            raise serializers.ValidationError(
                {
                    "detail": "The provided password is too weak. It should be at least 8 characters long.",
                    "code": "weak-password",
                }
            )
        return password

    def validate(self, data):
        data = super().validate(data)

        # Ensure phone_number is not provided for email-based user creation
        if data.get("phone_number"):
            raise serializers.ValidationError(
                _("Cannot provide a phone number when creating a user with an email.")
            )

        return data
