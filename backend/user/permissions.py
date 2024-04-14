from rest_framework import permissions


class ViewUserListPermission(permissions.BasePermission):
    message = 'Only Admins Or Staff Members Can View Users List.'
    def has_permission(self, request, view):
        
        return request.user.is_staff or request.user.is_superuser
    
class EditViewDetailPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj==request.user) or request.user.is_staff or request.user.is_superuser
    
class DeleteUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser