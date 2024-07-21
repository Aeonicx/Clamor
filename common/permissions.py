from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserBasedPermission(BasePermission):
    def has_permission(self, request, view):
        # Access is allowed only authenticated user
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Custom logic to determine if the user has permission to access the object
        # For example, you might check if the user is the owner of the object
        if request.user.is_superuser:
            return True
        elif request.user == obj.user:
            return True
        return False


class IsLoggedInOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access for non-authenticated users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Read-only access is allowed for all users
            return True

        # Full access is allowed only for authenticated users
        return request.user.is_authenticated


class IsSuperuserOrReadOnly(BasePermission):
    """
    Custom permission to allow superusers full access and read-only access to all other users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Read-only access is allowed for all users
            return True

        # Full access is allowed only for superusers
        return request.user.is_superuser
