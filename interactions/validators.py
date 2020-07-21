import json

from django.core.exceptions import ValidationError
from django import forms


def percentage_validator(percent: float) -> None:
    if not 0 <= percent <= 100.00:
        raise ValidationError('Please enter a valid percentage')


def json_validator(json_string: str) -> None:
    """ Takes a string as an input, and checks the following:
    1) If its in a valid json format
    2) That the json contains exactly 44 dictionaries
    3) That each dictionary contains only two elements
    4) That each answer choice is an integer among ``answer_choices``
    5) That each question dictionary has only two key-value pairs
    5) The question dictionary should contain keys among qn_attrs

    Any input which doesn't meet these standards is marked as invalid
    and a relevant ``ValidationError`` is raised. """

    answer_choices = [1, 2, 3, 4, 5]
    qn_attrs = ['subclass',  'factor']

    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError:
        raise ValidationError('Only json data accepted')
    if json_data:
        if not len(json_data) == 44:
            raise ValidationError('This group supports only 44 inputs')
        for dictionary in json_data:
            if len(dictionary) != 2:
                raise ValidationError(
                    'Only two key-value pairs allowed: question and answers'
                )
            if dictionary['answer_choice'] not in answer_choices:
                raise ValidationError(
                    f"{dictionary['answer_choice']} not among 1,2,3,4 or 5"
                )
            if len(dictionary['question']) != 2:
                raise ValidationError(
                    'Length of question dict should be 2 only'
                )
            for qn_attr in dictionary['question']:
                if qn_attr not in qn_attrs:
                    raise ValidationError(
                        f"Dictionary key should be among {qn_attrs}"
                    )
    else:
        raise ValidationError('The input seems to be corrupted')
