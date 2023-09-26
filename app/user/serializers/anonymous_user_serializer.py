from .base_user_serializer import BaseUserSerializer


class AnonymousUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["uid"]  # We only need to expose the UID for anonymous users.
        read_only_fields = ["uid"]
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True, "default": ""},
            "phone_number": {"required": False, "allow_blank": True, "default": ""},
            "password": {"required": False, "allow_blank": True, "default": ""},
        }

    def validate(self, data):
        # No specific validations needed for anonymous users.
        return data

    def create(self, validated_data):
        validated_data["is_anonymous"] = True
        return super().create(validated_data)
