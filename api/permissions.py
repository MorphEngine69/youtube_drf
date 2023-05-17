from django.shortcuts import get_object_or_404
from rest_framework import permissions

from videos.models import Profile


class IsProfileOrReadOnly(permissions.BasePermission):
    """Настройки разрешений для профиля."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Настройки разрешений для автора видео."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            request_profile = get_object_or_404(Profile, user=request.user)
            if obj.author == request_profile:
                return True
            else:
                return request.method in permissions.SAFE_METHODS
        else:
            return request.method in permissions.SAFE_METHODS


class FollowOrReadOnly(permissions.BasePermission):
    """Настройки разрешений для подписок на автора канала."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            request_profile = get_object_or_404(Profile, user=request.user)
            if obj.user == request_profile:
                return True
            else:
                return request.method in permissions.SAFE_METHODS
        else:
            return request.method in permissions.SAFE_METHODS
