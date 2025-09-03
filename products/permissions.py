from rest_framework.permissions import BasePermission


class IsShopPermission:
    def has_permission(self, request, view):
        return request.user.position.lower() == "shop"
