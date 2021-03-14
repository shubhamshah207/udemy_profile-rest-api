from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        """safe methods are the methods which do not change the object value"""
        if request.method in permissions.SAFE_METHODS:
            return True
        """If user is updating his own profile then this will be true"""
        return obj.id == request.user.id
