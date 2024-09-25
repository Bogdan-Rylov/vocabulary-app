from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import CustomLoginView, RegistrationView


app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
]
