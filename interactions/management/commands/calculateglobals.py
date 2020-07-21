import json

from django.core.management.base import BaseCommand, CommandError

from ...models import GlobalAverages, SelfAnswerGroup


class Command(BaseCommand):

    help = (
        'Calculate scores for each OCEAN SUBCLASS by querying all database '
        'entries, and create a GlobalAverage model instance. This is mainly '
        "used to calculate a user's percentile in single_result_view. "
    )

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Retrieve all entries from the database
        all_answers = SelfAnswerGroup.objects.all().values()

        # This dict will store all the scores in their corresponding subclass
        scores = {'openness': [], 'conscientiousness': [], 'extraversion': [],
                  'agreeableness': [], 'neuroticism': []}

        # Iterate over all entries and collect scores of individual subclasses
        # in ``scores``
        for answer in all_answers:
            # Since the answers were first converted to json and then saved as
            # a string in the model instance, therefore they need to be
            # converted back to a valid Python data type
            individual_score = answer['scores']
            scores['openness'].append(individual_score['openness'])
            scores['conscientiousness'].append(
                individual_score['conscientiousness']
            )
            scores['extraversion'].append(individual_score['extraversion'])
            scores['agreeableness'].append(individual_score['agreeableness'])
            scores['neuroticism'].append(individual_score['neuroticism'])

        self.stdout.write(self.style.SUCCESS('Finished collecting scores'))

        # Object is created here
        GlobalAverages.objects.create(
            openness=scores['openness'],
            conscientiousness=scores['conscientiousness'],
            extraversion=scores['extraversion'],
            agreeableness=scores['agreeableness'],
            neuroticism=scores['neuroticism']
        )

        self.stdout.write(self.style.SUCCESS('Job complete.'))
