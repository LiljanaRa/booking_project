from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsReviewAuthorOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
