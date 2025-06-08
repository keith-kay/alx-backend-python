from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view or edit it.
    Assumes the model instance has a `user` or `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to the owner only.
        return obj.user == request.user or getattr(obj, 'owner', None) == request.user