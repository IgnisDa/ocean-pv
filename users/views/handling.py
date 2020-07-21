from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views
from django.conf import settings

from users.forms import (
    RegistrationForm,
)
from core.decorators import check_recaptcha


class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_message = 'You can now login with your new credentials'
    extra_context = {'SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY}
    success_url = reverse_lazy('users:login')


class UserLoginView(auth_views.LoginView):
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated:
            messages.add_message(
                request, messages.INFO,
                'Login was successful!'
            )
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(auth_views.LogoutView):
    template_name = 'users/logout.html'
