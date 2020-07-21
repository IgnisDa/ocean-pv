from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView

from core.mixins import CustomLoginRequiredMixin
from ..functions import (
    return_ocean_descriptions_with_graph,
    return_plot_and_view_data,
    return_share_box, return_comparison_graphs
)
from ..forms import GraphSelector, AccuracySetterForm


class IndividualResultView(CustomLoginRequiredMixin, FormMixin, TemplateView):
    form_class = AccuracySetterForm
    template_name = 'graphs/single_result.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        plot, descriptions, percentiles = return_ocean_descriptions_with_graph(
            self.kwargs.get('pk')
        )
        context['plot'] = plot
        context['descriptions'] = descriptions
        context['percentiles'] = percentiles
        against = self.kwargs.get('pk')
        profile_pk = self.request.user.profile.pk
        context['share_box'] = return_share_box(
            self.request, profile_pk, against)

        return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        initial['pk'] = self.kwargs.get('pk')
        return initial


class ComparisonResultView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'graphs/comparison_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        plot, valid_dict, comparison_plot = return_comparison_graphs(
            self.kwargs['self_pk'], self.kwargs['relation_pk']
        )
        context['plot'] = plot
        context['valid_dict'] = valid_dict
        context['comparison_plot'] = comparison_plot
        return context


class MultipleResultView(CustomLoginRequiredMixin, FormMixin, TemplateView):
    template_name = 'graphs/multiple_results.html'
    form_class = GraphSelector

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    # def form_valid(self, form):
    #     print(form)
    #     primary_keys = list(
    #         primary_key for
    #         primary_key in form.cleaned_data.get('primary_key').split(',')
    #         if primary_key
    #     )

    #     view_dict = {
    #         'master': form.cleaned_data.get('answer_group'),
    #         'to_plot': primary_keys
    #     }

    #     valid_dict, unavailable_pks, duplicate_pks, plot = (
    #         return_plot_and_view_data(
    #             view_dict
    #         )
    #     )
    #     if unavailable_pks:
    #         messages.info(
    #             self.request,
    #             "Invalid entries and have been filtered out"
    #         )
    #     if duplicate_pks:
    #         messages.info(
    #             self.request,
    #             "Duplicate entries have been filtered out"
    #         )
    #     self.extra_context = {'plot': plot, 'valid_dict': valid_dict}
    #     return super().form_valid(form)


@login_required
def multiple_result_view(request):
    if request.method == 'POST':
        form = GraphSelector(request.user, request.POST)
        if form.is_valid():
            primary_keys = list(
                primary_key for
                primary_key in form.cleaned_data.get('primary_key').split(',')
                if primary_key
            )

            view_dict = {
                'master': form.cleaned_data.get('answer_group'),
                'to_plot': primary_keys
            }

            valid_dict, unavailable_pks, duplicate_pks, plot = (
                return_plot_and_view_data(
                    view_dict
                )
            )
            if unavailable_pks:
                messages.info(
                    request,
                    "Invalid entries and have been filtered out"
                )
            if duplicate_pks:
                messages.info(
                    request,
                    "Duplicate entries have been filtered out"
                )

            return render(request, 'graphs/multiple_results.html', {
                'form': form,
                'plot': plot, 'description_data': valid_dict
            })

    else:
        form = GraphSelector(request.user)
    return render(request, 'graphs/multiple_results.html', {
        'form': form,
    })


class GlobalResultsView(CustomLoginRequiredMixin, FormMixin, TemplateView):
    pass
