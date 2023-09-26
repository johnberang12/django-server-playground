from authentication.serializers.apple_obtain_pair_serializer import (
    AppleTokenObtainPairSerializer,
)
from authentication.serializers.email_obtain_pair_serializer import (
    EmailTokenObtainPairSerializer,
)
from authentication.serializers.facebook_obtain_pair_serializer import (
    FacebookTokenObtainPairSerializer,
)
from authentication.serializers.phone_obtain_pair_serializer import (
    PhoneTokenObtainPairSerializer,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# refresh token view
class CustomTokenRefreshView(TokenRefreshView):
    pass  # For now, we're not customizing the refresh behavior


# create token for email auth
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


# create token for phone auth
class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer


# create token for apple auth
class AppleTokenObtainPairView(TokenObtainPairView):
    serializer_class = AppleTokenObtainPairSerializer


# create token for facebook auth
class FacebookTokenObtainPairView(TokenObtainPairView):
    serializer_class = FacebookTokenObtainPairSerializer
