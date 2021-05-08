from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    """return true if permission to edit is there else false"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        """safe methods are the methods which do not change the object value"""
        if request.method in permissions.SAFE_METHODS:
            return True
        """If user is updating his own profile then this will be true"""
        """when you authenticate a request in django rest rest_framework it will assign the authenticated user profile to the request and we can use this to compare it to the object that is being updated"""
        return obj.id == request.user.id
