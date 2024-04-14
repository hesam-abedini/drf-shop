from rest_framework import permissions



    
class CreatePermission(permissions.BasePermission):

    message = 'Only Admins Or Staff Members Can Create This.'
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff or request.user.is_superuser
        

class CommentEditPermission(permissions.BasePermission):

    message="You Dont Have The Permission To Edit This Comment"

    def has_object_permission(self, request, view, obj):
        return (obj.user==request.user)
        
class CommentDeletePermission(permissions.BasePermission):

    message="You Dont Have The Permission To Delete This Comment"
    def has_object_permission(self, request, view, obj):
        return (obj.user==request.user) or request.user.is_staff or request.user.is_superuser