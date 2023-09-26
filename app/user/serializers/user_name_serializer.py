from core.models import UserName
from rest_framework import serializers


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserName
        fields = ["uid", "first", "middle", "last", "suffix"]
