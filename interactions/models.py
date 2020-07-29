import json

from django.db import models
try:
	from django.contrib.postgres.fields import JSONField
except ImportError:
	from django.db.models import JSONField
from users.models import UserProfile
from django.urls import reverse

from .validators import percentage_validator


class BaseAnswerGroup(models.Model):

    answer_date_and_time = models. DateTimeField(auto_now_add=True)
    self_user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='%(class)s_self')
    answers = JSONField(editable=False)
    accuracy = models.FloatField(
        null=True, blank=True,
        validators=[percentage_validator],
        editable=False
    )
    scores = JSONField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ This method extracts the ``answer_choice`` from ``self.answers``
        and then forms a scores ``dict`` which is saved in ``self.scores``
        attribute. This is done to reduce load on the server while calculating
        ``GlobalAverages``. """

        json_data = self.answers
        answers = [ans['answer_choice'] for ans in json_data]
        question_factors = [ans['question']['factor'] for ans in json_data]
        qn_subclasses = [ans['question']['subclass'] for ans in json_data]

        final_scores = [answer*question_factor for answer,
                        question_factor in zip(answers, question_factors)]

        scores = {'openness': 0, 'conscientiousness': 0, 'extraversion': 0,
                  'agreeableness': 0, 'neuroticism': 0}
        for final_score, question_subclass in zip(final_scores, qn_subclasses):
            if question_subclass == 'openness':
                scores['openness'] = (
                    scores['openness']
                    + final_score
                )
            elif question_subclass == 'conscientiousness':
                scores['conscientiousness'] = (
                    scores['conscientiousness']
                    + final_score
                )
            elif question_subclass == 'extraversion':
                scores['extraversion'] = (
                    scores['extraversion']
                    + final_score
                )
            elif question_subclass == 'agreeableness':
                scores['agreeableness'] = (
                    scores['agreeableness']
                    + final_score
                )
            elif question_subclass == 'neuroticism':
                scores['neuroticism'] = (
                    scores['neuroticism']
                    + final_score
                )
        self.scores = scores
        super().save(*args, **kwargs)

    def return_formatted_json(self):
        json_data = self.answers
        return json.dumps(json_data, indent=4, sort_keys=True)

    return_formatted_json.short_description = 'Formatted data'


class SelfAnswerGroup(BaseAnswerGroup):

    def __str__(self):
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse('graphs:single_result', kwargs={'pk': self.pk})


class RelationAnswerGroup(BaseAnswerGroup):
    attempted_against = models.ForeignKey(
        SelfAnswerGroup, on_delete=models.CASCADE,
        related_name='%(class)s_attempted',
    )
    relation_user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='%(class)s_relation',
    )

    def __str__(self):
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse(
            'graphs:comparison_view',
            kwargs={'self_pk': self.attempted_against.pk,
                    'relation_pk': self.pk}
        )


class GlobalAverages(models.Model):
    """ Contains the global information about different attributes like
    which can be used for plotting graphs of global scope. """

    openness = JSONField(editable=False)
    conscientiousness = JSONField(editable=False)
    extraversion = JSONField(editable=False)
    agreeableness = JSONField(editable=False)
    neuroticism = JSONField(editable=False)
    calculated_on = models.DateTimeField(
        auto_now=True, editable=False
    )

    class Meta:
        get_latest_by = "calculated_on"

    def __str__(self):
        return f"Averages for {self.calculated_on}"
