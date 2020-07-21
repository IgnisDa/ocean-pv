from django.shortcuts import redirect
from django.views.generic import TemplateView


def referral_view(request, profile_pk: int, against: int):

    request.session['profile_pk'] = profile_pk
    request.session['against'] = against
    return redirect('users:referral-instructions')


class ReferralInstructionsView(TemplateView):
    template_name = 'users/referral_instructions.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
