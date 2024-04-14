"""
serializers for user api view
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers
from user.models import Address
from user.validators import password_strength_validator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Permission
        fields=['id','codename']


class UpdatePermissionsSerializer(serializers.ModelSerializer):

    permission=serializers.ListField(child=serializers.CharField(),write_only=True)
    user_permissions=PermissionSerializer(many=True,required=False)
    class Meta:
        model=get_user_model()
        fields=['user_permissions','permission']
        read_only_fields = ['user_permissions']
        extra_kwargs = {'permission': {'write_only': True}}

    def update(self, instance, validated_data):

        perms=validated_data['permission']
        instance.user_permissions.clear()
        for perm in perms:
            perm_obj=Permission.objects.get(codename=perm)
            instance.user_permissions.add(perm_obj)
        instance.save()
        return instance
    

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        fields=['state','city','address_1','address_2','postal_code','phone_number']

class UserSerializer(serializers.ModelSerializer):
    user_permissions=PermissionSerializer(many=True,required=False)
    address=AddressSerializer()
    password=serializers.CharField(validators=[password_strength_validator],write_only=True,min_length=5)
    class Meta:
        model=get_user_model()
        fields=['id','email','password','name','user_permissions','address','is_active','is_staff','is_superuser']
        read_only_fields = ['user_permissions']
        extra_kwargs={'password':{'write_only':True},'is_staff':{'required':False},
                      'is_superuser':{'required':False},'is_active':{'required':False}}


    def create(self,validated_data):
        """create and return a user"""
        address_data=validated_data.pop('address',None)
        request=self.context.get('request')
        if request.user.is_superuser==False:
            validated_data.pop('is_staff',None)
            validated_data.pop('is_superuser',None)
        address=Address.objects.create(**address_data)
        user=get_user_model().objects.create_user(address=address,**validated_data)
        return user
    
    def update(self,instance,validated_data):
        password=validated_data.pop('password',None)
        address_data=validated_data.pop('address',None)
        request=self.context.get('request')
        if request.user.is_superuser==False:
            validated_data.pop('is_staff',None)
            validated_data.pop('is_superuser',None)
        if request.user.is_superuser==False and request.user.is_staff==False:
            validated_data.pop('is_active',None)
        user=super().update(instance,validated_data)
        if address_data is not None:
            address_obj=user.address
            for attr,value in address_data.items():
                setattr(address_obj,attr,value)
            address_obj.save()
        if password:
            user.set_password(password)
            user.save()


        return user
    


    
class EmailSerializer(serializers.Serializer):

    email=serializers.EmailField()

    class Meta:
        fields=['email']


class ResetPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(validators=[password_strength_validator],write_only=True,min_length=5)

    class Meta:
        fields=['password']

    def validate(self,data):
        password=data.get('password')
        token=self.context.get('kwargs').get('token')
        encoded_pk=self.context.get('kwargs').get('encoded_pk')
        if token is None or encoded_pk is None:
            raise serializers.ValidationError('Missing Data')
        pk=urlsafe_base64_decode(encoded_pk).decode()
        user=get_user_model().objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("The Reset Token Is Invalid")
        user.set_password(password)
        user.save()

        return data