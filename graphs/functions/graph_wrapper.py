from os import path
import json
import bisect

from interactions.models import (
    SelfAnswerGroup, RelationAnswerGroup, GlobalAverages
)
from .plotter import draw_plot, draw_comparison_plot
from .scores import update_dict_with_score, update_percentage_deviation


def return_valid_dict(pk: int) -> list:
    """ Makes a dict to be used in ``single_result_view`` """

    answer_group = SelfAnswerGroup.objects.get(pk=pk)
    valid_dict = [{
        'name': answer_group.self_user_profile.user.username,
        'master': True,
        'answer_group_pk': pk
    }]
    valid_dict = update_dict_with_score(valid_dict)

    return valid_dict


def return_descriptions(valid_dict: list) -> tuple:
    """ This constructs the file path to ``descriptions.json`` and then
    uses the ``valid_dict`` to match the scores from ``valid_dict`` and
    classify them as high or low and return the relevant descriptions. """

    file_dir = path.dirname(path.dirname(path.abspath(__file__)))
    file_path = path.join(file_dir, 'static',
                          'data', 'descriptions.json')
    with open(file_path) as f:
        json_data = json.load(f)

    averages = GlobalAverages.objects.latest()
    openness = averages.openness
    conscientiousness = averages.conscientiousness
    extraversion = averages.extraversion
    agreeableness = averages.agreeableness
    neuroticism = averages.neuroticism

    global_scores = {
        'openness': openness, 'conscientiousness': conscientiousness,
        'extraversion': extraversion, 'agreeableness': agreeableness,
        'neuroticism': neuroticism
    }

    for dictionary in valid_dict:
        dictionary.update({'descriptions': {}, 'percentiles': {}})
        scores = dictionary['score']
        for score in scores:
            for desc in json_data:
                if score == desc['subclass']:
                    position = bisect.bisect(
                        global_scores[score], scores[score])
                    percentile = (position/len(global_scores[score]))*100
                    dictionary['percentiles'].update(
                        {
                            score: round(percentile, 3)
                        }
                    )
                    if percentile > 50:
                        dictionary['descriptions'].update(
                            {
                                score: desc['descriptions']['high']
                            }
                        )
                    else:
                        dictionary['descriptions'].update(
                            {
                                score: desc['descriptions']['low']
                            }
                        )
    return valid_dict


def return_ocean_descriptions_with_graph(pk: int, *args, **kwargs) -> tuple:
    """ This is used for ``single_result_view`` to make a plot
    and then return the description of the personality related to that
    particular graph. """

    valid_dict = return_valid_dict(pk)
    valid_dict = return_descriptions(valid_dict)
    plot = draw_plot(valid_dict)
    for dictionary in valid_dict:
        descriptions = dictionary.pop('descriptions')
        percentiles = dictionary.pop('percentiles')

    return plot, descriptions, percentiles


def return_comparison_graphs(self_pk: int, relation_pk: int) -> tuple:
    """ Return a valid_dict containing two elements, one for the
    for the attempted test and the other for actual the actual test
    the said attempt was made against. """

    self_answer_group = SelfAnswerGroup.objects.get(pk=self_pk)
    relation_answer_group = RelationAnswerGroup.objects.get(pk=relation_pk)
    valid_dict = [
        {
            'name': self_answer_group.self_user_profile.user.username,
            'master': True,
            'answer_group_pk': self_pk,
            'score': self_answer_group.scores,
        },
        {
            'name': relation_answer_group.self_user_profile.user.username,
            'master': False,
            'answer_group_pk': relation_pk,
            'score': relation_answer_group.scores,
        }
    ]
    valid_dict = update_percentage_deviation(valid_dict)
    plot = draw_plot(valid_dict)
    comparison_plot = draw_comparison_plot(valid_dict)

    return plot, valid_dict, comparison_plot
