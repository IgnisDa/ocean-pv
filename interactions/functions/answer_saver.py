import json

from interactions.models import (
    SelfAnswerGroup,
    RelationAnswerGroup,
)
from users.models import UserProfile


def form_json_data(formset, questions: list) -> list:
    """ For each ``form`` in ``formset``, extracts the user's answer_choice
    and adds the question details along with its attributes as a dictionary.
    This is the actual data that is stored in the database as answer, after
    passing necessary validation. """

    json_data = []
    for form, question in zip(formset, questions):
        valid_dict = {
            'answer_choice': int(form.cleaned_data.get('answer_choice')),
            'question': {
                'subclass': question['subclass'],
                'factor': question['factor'],
                'number': question['number']
            }
        }
        json_data.append(valid_dict)

    json_data = json_data
    return json_data


def save_self_answers_to_db(json_data: list, request, *args, **kwargs) -> int:
    """ A function that takes json data (a list of dicts) and saves them to
    the database under the model of SelfAnswerGroup """

    answer_group = SelfAnswerGroup.objects.create(
        self_user_profile=request.user.profile,
        answers=json_data
    )

    return answer_group.pk


def save_relation_answers_to_db(
    json_data: list, request,  profile_pk: int,
    against_pk: int, *args, **kwargs
) -> int:
    """ A function that takes json data (a list of dicts) and saves them to
    the database under the model of RelationAnswerGroup """

    rel_profile = UserProfile.objects.get(pk=profile_pk)
    against = SelfAnswerGroup.objects.get(pk=against_pk)
    answer_group = RelationAnswerGroup.objects.create(
        self_user_profile=request.user.profile,
        answers=json_data,
        relation_user_profile=rel_profile,
        attempted_against=against
    )

    return answer_group.pk, answer_group.attempted_against.pk
