from django.urls import path

from accounts.views import CustomLoginView, RegistrationView


app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
]
