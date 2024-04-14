from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin



class Address(models.Model):

    state=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    address_1=models.TextField()
    address_2=models.TextField(blank=True,null=True)
    postal_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=20)

class UserManager(BaseUserManager):
    """manager for users"""

    def create_user(self,email,password=None,**extra_field):
        if not email:
            raise ValueError('user must have an email address')
        user=self.model(email=self.normalize_email(email),**extra_field)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password):
        user=self.create_user(email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """user in the system"""
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    address=models.OneToOneField(Address,on_delete=models.CASCADE,null=True)
    objects=UserManager()

    USERNAME_FIELD='email'





