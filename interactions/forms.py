import re

from django import forms
from django.forms import formset_factory

from .functions import return_questions
from interactions.models import SelfAnswerGroup
from users.models import UserProfile


class AnswerChoiceForm(forms.Form):

    CHOICES = (
        # ('Invalid', '-'*25),  # FIXME: Remove option before deployment # DONE
        (1, 'Disagree strongly'),
        (2, 'Disagree a little'),
        (3, 'Neither agree nor disagree'),
        (4, 'Agree a little'),
        (5, 'Agree strongly'),

    )
    answer_choice = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'style': 'width: 270px;'}
        ),
        choices=CHOICES,
        required=True
    )

    def clean_answer_choice(self):
        answer_choice = self.cleaned_data.get('answer_choice')
        if answer_choice is None or answer_choice == 'Invalid':
            raise forms.ValidationError('Please select a valid option')
        return answer_choice


AnswerFormset = formset_factory(
    AnswerChoiceForm, extra=len(return_questions('SelfAnswerGroup'))
)


class RelationSelectorForm(forms.Form):
    username = forms.CharField()


class ReferralCodeForm(forms.Form):
    referral_code = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'p:[number]-a:[number]'}
        ),
    )

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')
        pattern = "^p:[\d]+-a:[\d]+$"  # type: re
        if not re.search(pattern, referral_code):
            raise forms.ValidationError(
                ('You entered an invalid referral code'), code='invalid_regex'
            )
        profile_pk = int(referral_code.split('-')[0].lstrip('p:'))
        against = int(referral_code.split('-')[1].lstrip('a:'))
        if not (SelfAnswerGroup.objects.filter(pk=against).exists() or
                UserProfile.objects.filter(pk=profile_pk).exists()):
            raise forms.ValidationError(
                ('You entered an invalid referral code'), code='invalid_pks'
            )
        return referral_code

    def get_form_contents(self):
        referral_code = self.cleaned_data.get('referral_code')
        profile_pk = int(referral_code.split('-')[0].lstrip('p:'))
        against = int(referral_code.split('-')[1].lstrip('a:'))
        return profile_pk, against
