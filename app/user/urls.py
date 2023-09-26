"""
URL mappings for the user API
"""
from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path(
        "create-anonymous/",
        views.CreateAnonymousUserView.as_view(),
        name="create-anonymous",
    ),
    path("create-email/", views.CreateUserWithEmailView.as_view(), name="create-email"),
    path("create-phone/", views.CreateUserWithPhoneView.as_view(), name="create-phone"),
    path(
        "create-facebook/",
        views.CreateUserWithFacebookView.as_view(),
        name="create-facebook",
    ),
    path("create-apple/", views.CreateUserWithAppleView.as_view(), name="create-apple"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
