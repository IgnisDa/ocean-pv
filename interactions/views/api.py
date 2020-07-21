import random

from django.http import JsonResponse
from django.shortcuts import reverse
from django.db.models import Q, Max
from django.core import serializers

from users.models import UserProfile
from ..models import SelfAnswerGroup


def get_random_user():
    max_id = SelfAnswerGroup.objects.all().aggregate(
        max_id=Max("id")
    )['max_id']
    while True:
        pk = random.randint(1, max_id)
        user_profile = SelfAnswerGroup.objects.filter(pk=pk).first()
        if user_profile:
            return user_profile


def random_user_view(request):
    answer_group = get_random_user()
    if request.is_ajax() and request.method == "GET":
        profile_pk = answer_group.self_user_profile.pk
        against = answer_group.pk
        return_url = reverse(
            'interactions:taketest-relations',
            kwargs={'profile_pk': profile_pk, 'against': against}
        )
        response = {
            'return_url': return_url,
            'name': answer_group.self_user_profile.user.username
        }
        return JsonResponse(response)


def howto_relation_ajax(request):
    if request.is_ajax():
        username = request.GET.get('username', None)
        usernames = UserProfile.objects.filter(
            Q(user__username__contains=username)
        ).exclude(
            Q(user__username__exact=request.user.username) | Q(visible=False)
        )
        data = {
            'usernames': serializers.serialize('json', usernames)
        }
        if data['usernames']:
            data['exists'] = True
        return JsonResponse(data)
