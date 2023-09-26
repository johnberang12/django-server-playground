from rest_framework import permissions


class IsNotAnonymousUser(permissions.BasePermission):
    """
    Custom permission to only allow non-anonymous users to access the view.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated and not an anonymous user
        return (
            request.user
            and request.user.is_authenticated
            and not request.user.is_anonymous
        )
