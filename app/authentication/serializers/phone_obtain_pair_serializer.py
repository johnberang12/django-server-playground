from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from rest_framework import exceptions


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Check if phone number format is valid
        # You might want to use some library or regular expressions to validate phone number formats
        if not self.is_valid_phone_number(attrs.get("phone")):
            raise exceptions.AuthenticationFailed(
                {
                    "detail": "The phone number you provided doesn't appear to be in a proper format. Please double-check for any mistakes.",
                    "code": "invalid-phone-number-format",
                }
            )
        # ... additional validations specific to phone number sign-in

    @staticmethod
    def is_valid_phone_number(phone):
        # Check if the given phone number is in valid format
        # You can use regex or some library here to validate
        return True  # Placeholder, replace with actual logic
