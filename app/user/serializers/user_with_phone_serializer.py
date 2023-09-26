import phonenumbers
from user.serializers.base_user_serializer import BaseUserSerializer
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserWithPhoneSerializer(BaseUserSerializer):
    """Serializer for creating a user with a phone number."""

    class Meta(BaseUserSerializer.Meta):
        # We're inheriting fields from the BaseUserSerializer, so no need to redefine them
        extra_kwargs = {
            **BaseUserSerializer.Meta.extra_kwargs,
            "email": {"write_only": True, "required": False, "default": None},
            "phone_number": {"required": True},
            "password": {
                "write_only": True,
                "min_length": 5,
                "required": False,
                "default": None,
            },
        }

    def validate(self, data):
        data = super().validate(data)

        # Ensure email is not provided for phone-based user creation
        if data.get("email"):
            raise serializers.ValidationError(
                _("Cannot provide an email when creating a user with a phone number.")
            )

        # Validate phone number format
        phone_number = data.get("phone_number")
        if phone_number:
            try:
                parsed_number = phonenumbers.parse(phone_number, region="PH")
                if not phonenumbers.is_valid_number(parsed_number):
                    raise serializers.ValidationError(
                        _("The phone number provided is not valid.")
                    )
            except phonenumbers.NumberParseException:
                raise serializers.ValidationError(
                    _("The phone number provided is not valid.")
                )

        return data
