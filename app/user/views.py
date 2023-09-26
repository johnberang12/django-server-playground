"""
Views for the user API
"""
from user.serializers.base_user_serializer import BaseUserSerializer
from user.serializers.user_with_apple_serializer import UserWithAppleSerializer
from user.serializers.user_with_facebook_serializer import UserWithFacebookSerializer
from user.serializers.user_with_phone_serializer import UserWithPhoneSerializer
from user.serializers.user_with_email_serializer import UserWithEmailSerializer
from user.serializers.anonymous_user_serializer import AnonymousUserSerializer
from rest_framework.response import Response
from user.permissions import IsNotAnonymousUser
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateAnonymousUserView(generics.CreateAPIView):
    """Create an anonymous user in the system"""

    serializer_class = AnonymousUserSerializer


class CreateUserWithEmailView(generics.CreateAPIView):
    """Create a new user with email and password in the system"""

    serializer_class = UserWithEmailSerializer


class CreateUserWithPhoneView(generics.CreateAPIView):
    """Create a new user with phone number in the system"""

    serializer_class = UserWithPhoneSerializer


class CreateUserWithFacebookView(generics.CreateAPIView):
    """Create a new user with Facebook credentials in the system or log them in if they exist"""

    serializer_class = UserWithFacebookSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except APIException as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                data={"detail": str(e)},
                # Return the actual exception message for debugging
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateUserWithAppleView(generics.CreateAPIView):
    """Create a new user with Apple credentials in the system or log them in if they exist"""

    serializer_class = UserWithAppleSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except APIException as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = BaseUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsNotAnonymousUser]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
