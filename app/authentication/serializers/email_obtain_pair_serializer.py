from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # def validate(self, attrs):
    #     data = super().validate(attrs)

    #     # Add user's UID to the token payload
    #     data["uid"] = self.user.uid

    #     return data
    def validate(self, attrs):
        # Check if the email format is valid
        try:
            validate_email(attrs["email"])
        except ValidationError:
            raise exceptions.AuthenticationFailed(
                {
                    "detail": "The email address you provided doesn't appear to be in a proper format. Please double-check and enter a valid email address.",
                    "code": "invalid-email",
                }
            )

        # Call the original validate method to check for authentication
        try:
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed:
            # At this point, we know authentication failed but not why.
            # You can add additional checks to determine the exact reason.

            User = get_user_model()

            try:
                user = User.objects.get(email=attrs["email"])

                if not user.is_active:
                    raise exceptions.AuthenticationFailed(
                        {
                            "detail": "Your account has been temporarily disabled. Please contact support for assistance.",
                            "code": "user-disabled",
                        }
                    )
                # If we reach here, the email exists, but the password is wrong.
                raise exceptions.AuthenticationFailed(
                    {
                        "detail": "Your password doesn't match our records. Please double-check and try again.",
                        "code": "wrong-password",
                    }
                )
            except User.DoesNotExist:
                # Email not found in the database.
                raise exceptions.AuthenticationFailed(
                    {
                        "detail": "We couldn't find an account associated with this email. If you're new here, consider signing up!",
                        "code": "user-not-found",
                    }
                )

        return data
