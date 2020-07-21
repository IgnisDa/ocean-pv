from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured

from interactions.functions import (
    save_self_answers_to_db,
    save_relation_answers_to_db,
    find_similar_usernames,
    find_answer_groups_counts,
    get_data_fn,
    return_questions,
    form_json_data, send_relation_email
)
from interactions.forms import (
    RelationSelectorForm, ReferralCodeForm,
    AnswerFormset
)
from core.mixins import CustomLoginRequiredMixin


class HowtoView(TemplateView):
    template_name = 'interactions/howto_self.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.WARNING,
                'You are not logged in, you will be redirected to login'
            )
        return super().dispatch(request, *args, **kwargs)


class View(PermissionRequiredMixin, TemplateView):
    template_name = 'interactions/view.html'
    permission_required = ('users.special_access',)
    permission_denied_message = (
        'You do not have the required permissions to access that page'
    )
    raise_exception = True
    extra_context = {'data': get_data_fn()}


class BaseQuestionView(CustomLoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = AnswerFormset
    answer_group_model = None
    questions = None
    answer_saver = None
    success_message = 'Your answers were saved successfully'
    permission_denied_message = ('You have to be logged in to '
                                 'attempt the tests')

    def dispatch(self, request, *args, **kwargs):
        if not self.answer_group_model:
            raise ImproperlyConfigured(
                'Attribute answer_group_model set incorrectly. Valid '
                'options are SelfAnswerGroup and RelationsAnswerGroup.'
            )
        self.questions = return_questions(self.answer_group_model)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.questions
        return context

    def form_valid(self, formset):
        json_data = form_json_data(formset, self.questions)
        try:
            profile_pk = self.kwargs['profile_pk']
            against = self.kwargs['against']
        except KeyError:
            profile_pk = None
            against = None
        finally:
            request = self.request
        if self.answer_group_model == 'SelfAnswerGroup':
            answer_saver = save_self_answers_to_db
        elif self.answer_group_model == 'RelationAnswerGroup':
            answer_saver = save_relation_answers_to_db
        returned_data = answer_saver(
            json_data, request, profile_pk, against
        )
        try:
            if len(returned_data) == 2:
                primary_key, attempted_against = returned_data
                self.request.session['rel_ans_gp'] = primary_key
                self.success_url = reverse_lazy(
                    'graphs:comparison_view',
                    kwargs={'self_pk': attempted_against,
                            'relation_pk': primary_key}
                )
        except TypeError:
            self.request.session['self_ans_gp'] = returned_data
            self.success_url = reverse_lazy(
                'graphs:single_result', kwargs={'pk': returned_data}
            )
        return super().form_valid(formset)


class SelfQuestionView(BaseQuestionView):
    """ Displays the ``form`` which eventually saves all the answers in the
    database after necessary validation. The function ``return_questions``
    yields a list of questions which is present as a json file present in
    ``interactions/static/data/self_questions.json``. After a test is
    successfully attempted, a ``request.session['self_ans_gp']`` is set
    to the Test ID of the newly created test. This can be used for
    notification purposes on the results page. """

    template_name = 'interactions/questions.html'
    answer_group_model = 'SelfAnswerGroup'


class RelationQuestionView(BaseQuestionView):
    """ Same as ``SelfQuestionView`` with the difference that the questions
    sent are loaded from ``interactions/static/data/relation_questions.json``.
    A ``request.session['rel_ans_gp']`` set in this case. """

    template_name = 'interactions/questions.html'
    answer_group_model = 'RelationAnswerGroup'

    def get_success_url(self):
        primary_key = self.request.session['rel_ans_gp']
        email = send_relation_email(primary_key, self.request)
        return super().get_success_url()


class ReferralView(CustomLoginRequiredMixin, FormView):
    form_class = ReferralCodeForm
    template_name = 'interactions/howto_referral.html'

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        profile_pk, against = form.get_form_contents()
        self.success_url = reverse_lazy(
            'interactions:taketest-relations',
            kwargs={'profile_pk': profile_pk, 'against': against}
        )
        return super().form_valid(form)


@login_required
def howto_relations_view(request):
    if request.method == 'POST':
        form = RelationSelectorForm(request.POST)
        if form.is_valid():
            queryset = find_similar_usernames(form, request)
            answer_groups_counts = find_answer_groups_counts(queryset)
            context = {
                'form': form,
                'queryset': list(zip(queryset, answer_groups_counts))
            }
            if not queryset:
                messages.info(request, 'No such profile exists')
                return render(request, 'interactions/howto_relations.html',
                              context)
            if len(queryset) > 1:
                messages.info(
                    request, 'There are multiple profiles with that username')
                return render(request, 'interactions/howto_relations.html',
                              context)
            if len(queryset) == 1:
                messages.success(request, 'The requested profile was found!')
                return render(request, 'interactions/howto_relations.html',
                              context)
        else:
            messages.info(request, 'Please correct the errors below ')
    else:
        form = RelationSelectorForm(request.GET or None)
    return render(request, 'interactions/howto_relations.html', {'form': form})
