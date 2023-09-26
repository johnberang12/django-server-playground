from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from rest_framework import exceptions


class FacebookTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass
