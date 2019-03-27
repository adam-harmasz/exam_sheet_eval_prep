from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Not an owner."

    def has_object_permission(self, request, view, obj):
        """Defining permission only for an owner of an object"""
        if request.user == obj.owner or request.user.is_superuser:
            return True
        return False


class IsTeacher(permissions.BasePermission):
    message = "Not a teacher, only teachers have an access"

    def has_permission(self, request, view):
        """Defining permission only for an owner of an object"""
        return request.user.is_teacher
