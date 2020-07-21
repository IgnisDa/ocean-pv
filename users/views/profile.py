from django.shortcuts import render,    redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from users.forms import (
    ProfileUpdateForm,
    UserUpdateForm
)
from users.models import UserProfile
from core.mixins import CustomLoginRequiredMixin


@login_required
def update_profile_view(request, username):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO,
                             'You need to be logged in to edit your profile. ')
    instance = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, instance=instance)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.add_message(request, messages.INFO,
                                 'Your profile was updated successfully! ')
            url = reverse('users:profile', args=[request.user])
            return redirect(url)
        else:
            messages.add_message(request, messages.INFO,
                                 'Please correct the errors below')

    else:
        profile_form = ProfileUpdateForm(instance=instance)
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/userprofile_form.html', {
        'profile_form': profile_form,
        'user_form': user_form,
    })


class ProfileView(CustomLoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
