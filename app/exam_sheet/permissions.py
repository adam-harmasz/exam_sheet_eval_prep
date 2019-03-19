from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Not an owner."

    def has_object_permission(self, request, view, obj):
        """Defining permission only for an owner of an object"""

        return request.user == obj.owner
