from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    CustomTokenObtainPairView,
    LogoutView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("login/",           CustomTokenObtainPairView.as_view(), name="login"),
    path("register/",        RegisterView.as_view(),               name="register"),
    path("logout/",          LogoutView.as_view(),                 name="logout"),
    path("profile/",         ProfileView.as_view(),                name="profile"),
    path("change-password/", ChangePasswordView.as_view(),         name="change-password"),
    path("token/refresh/",   TokenRefreshView.as_view(),           name="token-refresh"),
]