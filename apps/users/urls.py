from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.contrib.auth import views as auth_views

from apps.users.views import (
    UserRegisterView,
    LogInAPIView,
    LogOutAPIView)


urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('auth-login/', LogInAPIView.as_view()),
    path('auth-logout/', LogOutAPIView.as_view()),
    path('auth-login-jwt/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
    path('web-login/', auth_views.LoginView.as_view(), name='login'),
    path('web-logout/', auth_views.LogoutView.as_view(), name='logout'),
]
