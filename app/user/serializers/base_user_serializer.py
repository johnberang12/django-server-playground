"""
Seralizers for the user API View
"""

from django.contrib.auth import get_user_model


from django.utils.translation import gettext as _

from rest_framework import serializers


class BaseUserSerializer(serializers.ModelSerializer):
    """Base serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "phone_number"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "email": {"required": False},
            "phone_number": {"required": False},
        }

    def create(self, validated_data):
        """Common user creation logic"""
        print("Initial data:", self.initial_data)  # Raw data from the request
        print("Validated data:", validated_data)
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        phone_number = validated_data.pop("phone_number", None)
        facebook_token = validated_data.pop("facebook_token", None)
        apple_token = validated_data.pop("apple_token", None)
        # Determine the type of user creation based on the validated data
        if email and password:
            user = get_user_model().objects.create_user_with_email_and_password(
                email=email,
                password=password,
                **validated_data,
            )
        elif phone_number:
            user = get_user_model().objects.create_user_with_phone_number(
                phone_number=phone_number, **validated_data
            )
            user.set_unusable_password
        elif facebook_token:
            user = get_user_model().objects.create_user_with_facebook(
                facebook_token=facebook_token, **validated_data
            )
        elif apple_token:
            user = get_user_model().objects.create_user_with_apple(
                apple_token=apple_token, **validated_data
            )
        else:
            # Anonymous user creation
            user = get_user_model().objects.create_anonymous_user()
        return user

    def update(self, instance, validated_data):
        """Common update logic for all users"""
        password = validated_data.pop("password", None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
