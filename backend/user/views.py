from rest_framework import generics,permissions,status
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from rest_framework import filters

from app.pagination import StandardResultsSetPagination
from user.serializers import (UserSerializer,PermissionSerializer,UpdatePermissionsSerializer,
                              EmailSerializer,ResetPasswordSerializer)
from user.permissions import ViewUserListPermission,EditViewDetailPermission,DeleteUserPermission



class PermissionListView(generics.ListAPIView):
    serializer_class=PermissionSerializer
    queryset=Permission.objects.all()


class UpdateUserPermissions(generics.UpdateAPIView):
    serializer_class=UpdatePermissionsSerializer
    queryset=get_user_model().objects.all()

class ListUserView(generics.ListAPIView):
    search_fields = ['name','email']
    ordering_fields = ['name','email','is_active','is_staff','is_superuser']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    serializer_class=UserSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,ViewUserListPermission]
    queryset=get_user_model().objects.all()
    pagination_class=StandardResultsSetPagination

    def get_queryset(self):
        queryset=self.queryset
        is_staff=self.request.query_params.get('is_staff')
        is_active=self.request.query_params.get('is_active')
        is_superuser=self.request.query_params.get('is_superuser')
        state=self.request.query_params.get('state')
        city=self.request.query_params.get('city')
        if is_staff:
            try:
                is_staff=bool(int(is_staff))
            except ValueError:
                is_staff=True
            queryset=queryset.filter(is_staff=is_staff)
        if is_active:
            try:
                is_active=bool(int(is_active))
            except ValueError:
                is_active=True
            queryset=queryset.filter(is_active=is_active)
        if is_superuser:
            try:
                is_superuser=bool(int(is_superuser))
            except ValueError:
                is_superuser=True
            queryset=queryset.filter(is_superuser=is_superuser)
        if state:
            queryset=queryset.filter(address__state=state)
        if city:
            queryset=queryset.filter(address__city=city)
        return queryset.all().order_by('id')



class CreateUserView(generics.CreateAPIView):
    serializer_class=UserSerializer




class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,EditViewDetailPermission]
    queryset=get_user_model().objects.all()
    # def get_object(self):
    #     return self.request.user

class DeleteUserView(generics.DestroyAPIView):
    serializer_class=UserSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,DeleteUserPermission]
    queryset=get_user_model().objects.all()

class PasswordResetRequestView(generics.GenericAPIView):
    
    serializer_class=EmailSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data['email']
        user=get_user_model().objects.filter(email=email).first()
        if user:
            encoded_pk=urlsafe_base64_encode(force_bytes(user.pk))
            token=PasswordResetTokenGenerator().make_token(user)
            reset_url=reverse('user:reset-password',
                              kwargs={'encoded_pk':encoded_pk,'token':token})
            reset_url=f'http://localhost:8000/{reset_url}'
            return Response(
                {
                    'message':f'your password reset link is: {reset_url}'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({
                'message':'user does not exists'
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
class PasswordResetView(generics.GenericAPIView):
    serializer_class=ResetPasswordSerializer

    def patch(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'kwargs':kwargs})
        serializer.is_valid(raise_exception=True)

        return Response({
            'message':'password reset Complete'
        },
        status=status.HTTP_200_OK
        )

