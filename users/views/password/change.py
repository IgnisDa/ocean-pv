from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from core.mixins import CustomLoginRequiredMixin


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was updated successfully! ')
            return redirect(reverse('users:password-change-done'))
        else:
            messages.info(request, 'Please correct the errors below ')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change_form.html', {'form': form})


class UserPasswordChangeDoneView(
    CustomLoginRequiredMixin, auth_views.PasswordChangeDoneView
):
    template_name = 'users/password_change_done.html'
