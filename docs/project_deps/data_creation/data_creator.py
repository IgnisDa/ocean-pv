""" This module can be used to create users for initial setup. Run
`cat docs/project_deps/data_creation/data_creator.py | python manage.py shell`
to use this. Remember to change USERNAME_LIST to change usernames. """

from django.contrib.auth.models import User

from interactions.models import SelfAnswerGroup, RelationAnswerGroup
from interactions.functions import return_questions

import random
import json

SUPERUSER = 'ignisda'
USERNAME_LIST = [str(x) for x in range(10, 20)]

for username in USERNAME_LIST:
    print(f"Processing {username}")
    user = User.objects.create_user(
        username=username,
        password='test-pass'
    )
    user.save()
print('Users done')

for _ in range(10):
    profile = User.objects.get(username=SUPERUSER).profile
    json_data = []
    for question in return_questions('SelfAnswerGroup'):
        valid_dict = {
            'answer_choice': random.randint(1, 5),
            'question': {
                'subclass': question['subclass'],
                'factor': int(question['factor'])
            }
        }
        json_data.append(valid_dict)

    SelfAnswerGroup.objects.create(
        self_user_profile=profile,
        answers=json.dumps(json_data)
    )
print('self done')
for _ in range(10):
    attempted_against = SelfAnswerGroup.objects.get(pk=1)
    self_profile = User.objects.get(username=SUPERUSER).profile
    relation_profile = User.objects.get(
        username=random.choice(USERNAME_LIST)
    ).profile
    print(f"Processing {relation_profile.user.username}")
    json_data = []
    for question in return_questions('RelationAnswerGroup'):
        valid_dict = {
            'answer_choice': random.randint(1, 5),
            'question': {
                'subclass': question['subclass'],
                'factor': int(question['factor'])
            }
        }
        json_data.append(valid_dict)

    RelationAnswerGroup.objects.create(
        relation_user_profile=relation_profile,
        attempted_against=attempted_against,
        self_user_profile=self_profile,
        answers=json.dumps(json_data)
    )
print('relation done')
