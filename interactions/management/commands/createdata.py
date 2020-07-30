import json
import string
import random

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from ...models import SelfAnswerGroup, RelationAnswerGroup
from interactions.functions import return_questions


def generate_random_string(size: int) -> str:
    random_string = ''.join(
        [random.choice(string.ascii_letters) for _ in range(size)]
    )
    return random_string


def create_json_data(answer_group: str) -> str:
    json_data = []
    for question in return_questions(answer_group):
        json_data.append(
            {
                'answer_choice': random.randint(1, 5),
                'question': {
                    'subclass': question['subclass'],
                    'factor': question['factor'],
                    'number': question['number']
                }
            }
        )
    return json_data


class Command(BaseCommand):

    help = (
        'Creates some data for the initial setup. Adds relevant data to '
        'the database. Note: At least one superuser should be present in the '
        'database otherwise an error would be raised.'
    )

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-a', '--all', action='store_true',
            help=(
                'Whether data should be added to all the models. '
                'Defaults to true'
            )
        )
        group.add_argument(
            '-e', '--exclude', nargs='+',
            help=(
                'Which models should be populated with random data'
            )
        )
        parser.add_argument(
            'superuser',
            help=(
                'The username of the superuser. If not present in '
                'the database, an error is raised'
            )
        )
        parser.add_argument(
            '-p', '--password', default='test-pass', type=str,
            help=(
                'The password of all the created users will be set to '
                'this if specified. Otherwise the default password '
                "'test-pass' is used"
            )
        )
        parser.add_argument(
            '--num-users', default=30, type=int, dest='num_users',
            help=(
                'The number of users to be created. Defaults to 30'
            )
        )
        parser.add_argument(
            '--num-self', default=30, type=int, dest='num_self',
            help=(
                'The number of SelfAnswerGroups to be created. '
                'Defaults to 30. All of them are owned by superuser'
            )
        )
        parser.add_argument(
            '--num-rel', default=30, type=int, dest='num_rel',
            help=(
                'The number of RelationAnswerGroup to be created. '
                'Defaults to 30. All of them are attempted by superuser '
                'and they are attempted for a random user from the '
                'users just created before'
            )
        )
        parser.add_argument(
            '--num-others', default=30, type=int, dest='num_others',
            help=(
                'The number of RelationAnswerGroup to be created. '
                'Defaults to 30. All of them are attempted by random '
                'users from the users just created before'
            )
        )
        parser.add_argument(
            '--string-size', default=30, type=int, dest='string_size',
            help=(
                'The size of the names of the new users created. '
                'Defaults to 30'
            )
        )

    def handle(self, *args, **options):
        superuser = options['superuser']
        try:
            superuser = User.objects.get(username=superuser)
        except User.DoesNotExist:
            raise CommandError(
                f"The user with the username {superuser} does not exist"
            )
        if not superuser.is_superuser:
            raise CommandError(
                f"User with the username {superuser} is not a superuser"
            )
        all = options['all']
        exclude = options['exclude']
        password = options['password']
        num_users = options['num_users']
        num_self = options['num_self']
        num_rel = options['num_rel']
        num_others = options['num_others']
        string_size = options['string_size']

        new_users = []
        for index, _ in enumerate(range(num_users), 1):
            username = generate_random_string(string_size)
            first_name = generate_random_string(string_size)
            last_name = generate_random_string(string_size)
            email = f"{generate_random_string(string_size)}@email.com"
            new_users.append(
                User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
            )
            self.stdout.write(
                f'{index}: Created user with username ', ending='')
            self.stdout.write(self.style.SUCCESS(f"{username}"))

        new_self_answers = []
        self.stdout.write('')
        for index, _ in enumerate(range(num_self), 1):
            profile = superuser.profile
            json_data = create_json_data('SelfAnswerGroup')

            new_self_answers.append(
                SelfAnswerGroup.objects.create(
                    self_user_profile=profile,
                    answers=json_data
                )
            )
            self.stdout.write(
                f'{index}: Created SelfAnswerGroup for ', ending='')
            self.stdout.write(self.style.SUCCESS(f"{profile}"))

        self.stdout.write('')
        for index, _ in enumerate(range(num_self), 1):
            profile = random.choice(new_users).profile
            json_data = create_json_data('SelfAnswerGroup')

            new_self_answers.append(
                SelfAnswerGroup.objects.create(
                    self_user_profile=profile,
                    answers=json_data
                )
            )
            self.stdout.write(
                f'{index}: Created SelfAnswerGroup for ', ending='')
            self.stdout.write(self.style.SUCCESS(f"{profile}"))

        new_rel_answers = []
        self.stdout.write('')
        for index, _ in enumerate(range(num_rel), 1):
            relation_profile = random.choice(new_users).profile
            self_profile = superuser.profile
            attempted_against = random.choice(new_self_answers)
            json_data = create_json_data('RelationAnswerGroup')

            new_rel_answers.append(
                RelationAnswerGroup.objects.create(
                    self_user_profile=self_profile,
                    relation_user_profile=relation_profile,
                    attempted_against=attempted_against,
                    answers=json_data
                )
            )
            self.stdout.write(
                f'{index}: Created RelationAnswerGroup with relation to ',
                ending=''
            )
            self.stdout.write(self.style.SUCCESS(
                f"{relation_profile}"
            ))

        new_others_answers = []
        self.stdout.write('')
        for index, _ in enumerate(range(num_others), 1):
            self_profile = random.choice(new_users).profile
            relation_profile = superuser.profile
            attempted_against = random.choice(new_self_answers)
            json_data = create_json_data('RelationAnswerGroup')

            new_others_answers.append(
                RelationAnswerGroup.objects.create(
                    self_user_profile=self_profile,
                    relation_user_profile=relation_profile,
                    attempted_against=attempted_against,
                    answers=json_data
                )
            )
            self.stdout.write(
                f'{index}: Created RelationAnswerGroup attempted by ',
                ending=''
            )
            self.stdout.write(self.style.SUCCESS(
                f"{self_profile}"
            ))
