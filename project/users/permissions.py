from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, "action_permissions", {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same."""
        return request.user == obj
