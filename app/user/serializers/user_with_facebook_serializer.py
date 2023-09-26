from core.models import ProviderData, User
from user.utils import validate_facebook_token
from user.serializers.base_user_serializer import BaseUserSerializer
from rest_framework import serializers


class UserWithFacebookSerializer(BaseUserSerializer):
    """Serializer for creating a user with Facebook credentials"""

    facebook_id = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True, required=False
    )  # Make password optional

    class Meta(BaseUserSerializer.Meta):
        # Extend the fields from BaseUserSerializer
        fields = BaseUserSerializer.Meta.fields + ["facebook_id"]
        extra_kwargs = {"facebook_id": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data.get("email")
        facebook_id = validated_data.get("facebook_id")

        # Attempt to retrieve the existing ProviderData object
        provider_data = ProviderData.objects.filter(
            provider="facebook", provider_id=facebook_id
        ).first()

        if provider_data and provider_data.user:
            # If the ProviderData entry exists and has an associated user, return that user
            return provider_data.user
        else:
            # If it doesn't exist, create the associated User object first
            user = User.objects.create(email=email)

            # Then create the ProviderData object be cause its obviously not exist
            ProviderData.objects.create(
                provider="facebook", provider_id=facebook_id, user=user, metadata={}
            )
            return user

    def validate(self, data):
        token = data.get("facebook_id")
        email = validate_facebook_token(token)
        data["email"] = email

        return data
