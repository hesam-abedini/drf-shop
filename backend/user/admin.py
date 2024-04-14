from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user import models

class UserAdmin(BaseUserAdmin):
    """define admin page for users"""
    ordering=['id']
    list_display=['id','email','name']
    fieldsets=(
        (None,{'fields':('email','password')}),
        (
            'permissions',
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        ('important dates',{'fields':('last_login',)})
    )
    readonly_fields=['last_login']
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

admin.site.register(models.User,UserAdmin)