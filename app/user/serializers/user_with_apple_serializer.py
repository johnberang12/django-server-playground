from core.models import ProviderData, User
from user.serializers.base_user_serializer import BaseUserSerializer
from rest_framework import serializers
from user.utils import validate_apple_token


class UserWithAppleSerializer(BaseUserSerializer):
    """Serializer for creating a user with Apple credentials"""

    apple_id = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True, required=False
    )  # Make password optional

    class Meta(BaseUserSerializer.Meta):
        # Extend the fields from BaseUserSerializer
        fields = BaseUserSerializer.Meta.fields + ["apple_id"]
        extra_kwargs = {"apple_id": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data.get("email")
        apple_id = validated_data.get("apple_id")

        # Attempt to retrieve the existing ProviderData object
        provider_data = ProviderData.objects.filter(
            provider="apple", provider_id=apple_id
        ).first()

        if provider_data and provider_data.user:
            # If the ProviderData entry exists and has an associated user, return that user
            return provider_data.user
        else:
            # If it doesn't exist, create the associated User object first
            user = User.objects.create(email=email)

            # Then create the ProviderData object because it obviously doesn't exist
            ProviderData.objects.create(
                provider="apple", provider_id=apple_id, user=user, metadata={}
            )

            # Return a 201 Created response for new user creation

            return user

    def validate(self, data):
        token = data.get("apple_id")
        email = validate_apple_token(
            token
        )  # Assuming you have a similar function for Apple
        data["email"] = email

        return data
