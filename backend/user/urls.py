"""
url mappings for user api
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user import views

app_name='user'

urlpatterns = [
    path('',views.ListUserView.as_view()),
    path('password-reset/',views.PasswordResetRequestView.as_view()),
    path('password-reset/<str:encoded_pk>/<str:token>/',views.PasswordResetView.as_view(),name='reset-password'),
    path('<int:pk>/update/',views.UpdateUserPermissions.as_view()),
    path('<int:pk>/delete/',views.DeleteUserView.as_view()),
    path('create/',views.CreateUserView.as_view(),name='create'),
    path('token/',TokenObtainPairView.as_view(),name='token'),
    path('<int:pk>/',views.ManageUserView.as_view(),name='update'),
    path('perm/',views.PermissionListView.as_view(),name='perm')
]
