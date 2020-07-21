from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

# TODO: Fix html_email_template.html


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy('users:password-reset-done')
    template_name = 'users/password_reset/password_reset_form.html'
    email_template_name = 'users/password_reset/password_reset_email.html'
    subject_template_name = 'users/password_reset/password_reset_subject.txt'
    html_email_template_name = 'users/password_reset/html_email_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website_address = self.request.get_host()
        receiver_name = self.request.user.username
        context.update({
            'receiver_name': receiver_name,
            'website_address': website_address
        })
        return context


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('users:password-reset-complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset/password_reset_complete.html'
