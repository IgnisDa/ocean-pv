import random
import json

import pytest
from django.core.management import call_command

from interactions.models import (
    SelfAnswerGroup,
    RelationAnswerGroup,
)
from interactions.functions import return_questions


@pytest.fixture()
def create_self_answers():

    def _create_answers(user):
        json_data = []
        for question in return_questions('SelfAnswerGroup'):
            valid_dict = {
                'answer_choice': random.randint(1, 5),
                'question': {
                    'subclass': question['subclass'],
                    'factor': question['factor']
                }
            }
            json_data.append(valid_dict)

        answer_group = SelfAnswerGroup.objects.create(
            self_user_profile=user.profile,
            answers=json_data
        )
        return answer_group.pk

    return _create_answers


@pytest.fixture
def create_averages():

    def _create_averages():
        call_command('calculateglobals')

    return _create_averages
