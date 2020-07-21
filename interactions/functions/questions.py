import json
import random
from os import path


def return_questions(model: str) -> list:
    """ This loads the questions from ``interactions/static/data/*.json`` as
    per requirement and raises an ``Exception`` if the requested question
    is not among the ones available. """

    if model == 'SelfAnswerGroup':
        file = 'self_questions'
    elif model == 'RelationAnswerGroup':
        file = 'relation_questions'
    else:
        raise Exception(
            (f"Invalid model ({model}) used."
             " Only SelfAnswerGroup and RelationAnswerGroup allowed.")
        )
    file_path = path.dirname(path.dirname(__file__))
    with open(path.join(file_path, 'static', 'data', f"{file}.json")) as f:
        json_data = json.load(f)
        random.shuffle(json_data)
        return json_data
