from django.urls import path
from .views import (
    AppleTokenObtainPairView,
    EmailTokenObtainPairView,
    CustomTokenRefreshView,
    FacebookTokenObtainPairView,
    PhoneTokenObtainPairView,
)

app_name = "authentication"

urlpatterns = [
    path(
        "email-token-obtain-pair/",
        EmailTokenObtainPairView.as_view(),
        name="email-token-obtain-pair",
    ),
    path(
        "phone-token-obtain-pair/",
        PhoneTokenObtainPairView.as_view(),
        name="phone-token-obtain-pair",
    ),
    path(
        "apple-token-obtain-pair/",
        AppleTokenObtainPairView.as_view(),
        name="apple-token-obtain-pair",
    ),
    path(
        "facebook-token-obtain-pair/",
        FacebookTokenObtainPairView.as_view(),
        name="facebook-token-obtain-pair",
    ),
    path("token-refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
]
