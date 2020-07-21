from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages

from ..models import RelationAnswerGroup


def send_relation_email(primary_key: int, request) -> None:
    answer_group = RelationAnswerGroup.objects.get(pk=primary_key)
    user_email = answer_group.relation_user_profile.user.email
    user_name = answer_group.self_user_profile.user.username
    user = answer_group.relation_user_profile.user.username
    website_address = request.get_host()
    if not user_email:
        messages.add_message(
            request, messages.INFO,
            f"{user_name} doesn't have a valid email registered "
            'and will not be sent any notification'
        )
        return
    from_email = settings.EMAIL_HOST_USER
    subject = f'Your peer {user_name} tried to guess your personality!'
    message = (
        f"{user_name} tried to guess your personality. Want to know how "
        f"accurate they were? Visit {website_address} to see some pretty "
        'graphs describing their test and then rate their accuracy. And while '
        f"you are there, you can attempt a test guessing {{user_name}}"
        "personality. Or maybe, why don't you attempt another test to see how "
        'much your own personality changed from the last time?'
    )
    html_message = 'emails/test_attempted.html'
    context = {
        'user_name': user_name, 'user': user,
        'website_address': website_address
    }
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[user_email],
        html_message=render_to_string(html_message, context=context),
        fail_silently=False,
    )
    messages.add_message(
        request, messages.INFO,
        f"{user_name} has been sent an email notifying them about "
        'your test attempt'
    )
    return
