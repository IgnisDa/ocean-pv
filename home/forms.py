from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        required=True,
        label='Email ID',
        widget=forms.TextInput()
    )

    subject = forms.CharField(
        required=True,
        label='Email Subject',
        widget=forms.TextInput()
    )
    message = forms.CharField(
        required=True,
        label='Email Body',
        widget=forms.Textarea(attrs={'style': 'height: 150px'})
    )

    def send_email(self, *args, **kwargs):
        from_email = self.cleaned_data.get('from_email').strip()
        subject = self.cleaned_data.get('subject').strip()
        message = self.cleaned_data.get('message')
        context = {'user_name': from_email, 'message':message,
        'user': from_email, 'website_address': 'ocean-pv', 'subject': subject}
        html_message = render_to_string('emails/contact.html', context)

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[settings.EMAIL_HOST_USER] if
            settings.EMAIL_HOST_USER else ['ocean-pv_dev@email.com'],
            html_message=html_message,
            fail_silently=False,
        )
