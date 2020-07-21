from django.db.models import Q

from users.models import UserProfile
from interactions.models import SelfAnswerGroup


def find_similar_usernames(form: dict, request) -> list:
    """ Finds similar usernames to the ones specified in ``form`` while
    also excluding the user actually performing the search. """

    username = form.cleaned_data.get('username').strip().lower()
    queryset = UserProfile.objects.filter(
        Q(user__username__contains=username)
    ).exclude(
        Q(user__username__exact=request.user.username) | Q(visible=False)
    )

    return queryset


def find_answer_groups_counts(queryset: list) -> list:
    """ Find the number of tests attempted by each user in the ``queryset`` and
    return a corresponding list. """

    answer_groups = [SelfAnswerGroup.objects.filter(
        self_user_profile__exact=profile
    ).count() for profile in queryset]

    return answer_groups
