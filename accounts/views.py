from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from accounts.forms import (
    CustomAuthenticationForm,
    RegistrationForm,
    ProfileForm,
)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("vocabulary:home")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            # Set session to expire when the browser is closed
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            # Set session to expire in 30 minutes
            self.request.session.set_expiry(0)

        login(self.request, form.get_user())
        return redirect(self.get_success_url())


class RegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("vocabulary:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

        return super().form_valid(form)


class CreateProfileView(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    template_name = "accounts/create_profile.html"
    success_url = reverse_lazy("vocabulary:home")

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "profile"):
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)
