from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from interactions.models import (
    SelfAnswerGroup,
    RelationAnswerGroup
)
from core.mixins import CustomLoginRequiredMixin


@login_required
def result_view(request, username):
    self_answer_groups = SelfAnswerGroup.objects.filter(
        self_user_profile=request.user.profile
    ).order_by('-answer_date_and_time')[:15]
    relation_answer_groups = RelationAnswerGroup.objects.filter(
        self_user_profile=request.user.profile).order_by(
            '-answer_date_and_time'
    )[:15]
    others_answer_groups = RelationAnswerGroup.objects.filter(
        relation_user_profile=request.user.profile).order_by(
            '-answer_date_and_time'
    )[:15]
    return render(
        request, 'users/results.html', {
            'self_answer_groups': self_answer_groups,
            'relation_answer_groups': relation_answer_groups,
            'others_answer_groups': others_answer_groups
        }
    )


class UserSelfAnswerGroupsListView(CustomLoginRequiredMixin, ListView):
    template_name = 'users/selfanswergroup_list.html'
    answer_group_model = SelfAnswerGroup
    paginate_by = 15

    def get_queryset(self):
        return self.answer_group_model.objects.filter(
            self_user_profile=self.kwargs['profile_pk']
        ).order_by('-answer_date_and_time')


class SelfAnswerGroupsListView(UserSelfAnswerGroupsListView):
    template_name = 'users/selfanswergroup_choice_view.html'
    answer_group_model = SelfAnswerGroup


class UserRelationAnswerGroupsListView(UserSelfAnswerGroupsListView):
    template_name = 'users/relationanswergroup_list.html'
    answer_group_model = RelationAnswerGroup

    def get_queryset(self):
        return self.answer_group_model.objects.filter(
            relation_user_profile=self.kwargs['profile_pk']
        ).order_by('-answer_date_and_time')


class UserOthersAnswerGroupsListView(UserSelfAnswerGroupsListView):
    template_name = 'users/othersanswergroup_list.html'
    answer_group_model = RelationAnswerGroup
