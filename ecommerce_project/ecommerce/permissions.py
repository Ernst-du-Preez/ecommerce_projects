"""
Custom DRF permissions for role-based access control.
"""
from rest_framework import permissions


class IsVendorOrReadOnly(permissions.BasePermission):
    """
    Vendors can create/edit/delete their own stores and products.
    Others can only read.
    """
    def has_permission(self, request, view):
        # Read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated vendors
        return request.user.is_authenticated and request.user.groups.filter(name='Vendor').exists()
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for the owner (vendor)
        if hasattr(obj, 'vendor'):
            return obj.vendor == request.user
        elif hasattr(obj, 'store'):
            return obj.store.vendor == request.user
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'vendor'):
            return obj.vendor == request.user
        elif hasattr(obj, 'store'):
            return obj.store.vendor == request.user
        
        return False


class IsAuthenticatedVendor(permissions.BasePermission):
    """
    Permission for vendor-only actions.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Vendor').exists()
        )
