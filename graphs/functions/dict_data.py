from os import path
import json

from django.shortcuts import reverse

from .cleaner import clean_multiple_results_data
from .scores import update_dict_with_score
from .plotter import draw_plot
from .percentages import (
    calculate_areas,
    calculate_percentages
)


def return_plot_and_view_data(view_dict: dict, *args, **kwargs) -> tuple:
    """ This function will take in a dict with 2 keys 'master' and
    'primary_keys' from 'multiple_result_view'
    and do the following:
    1) clean up the data for unavailable and duplicate keys
    2) create and returns the plot
    3) calculates the areas and the percentage difference

    It will return a tuple of the following format:
    (
        {
            'name': str,
            'master': bool,
            'percentage': float,
            'answer_group_pk': int
        }, plot
    ) """

    valid_dict, unavailable_pks, duplicate_pks = clean_multiple_results_data(
        view_dict['master'], *view_dict['to_plot'])
    valid_dict = update_dict_with_score(valid_dict)
    plot = draw_plot(valid_dict)
    valid_dict = calculate_percentages(calculate_areas(valid_dict))

    return valid_dict, unavailable_pks, duplicate_pks, plot


def return_share_box(request, profile_pk, against) -> dict:
    """
    Use json at ``file_path`` to form a ``dict`` used in ``single_result_view``
    to render the ``share-box`` html. This contains links to invite new
    users to the website via various platforms, currently: Facebook, Reddit,
    Telegram, WhatsApp and via mail.
    """

    link = reverse('users:referral-instructions')
    try:
        host = request.META['HTTP_HOST']
    except KeyError:
        # The application is being run in a test environment,
        # skip any issues
        host = None
    link = f"{request.scheme}://{host}{link}"
    name = (request.user.first_name if request.user.first_name
            else request.user.username)
    referral_code = f"p:{profile_pk}-a:{against}"
    body = (
        f"Your peer {name} is inviting you to guess their personality. "
        "Enter the referral code to attempt a simple test to see "
        "how well you know them. On completion, you will be presented with a "
        "simple graph which shows your attempt in comparison to their own. "
        f"Get started now at: {link}. Referral code is {referral_code}"
    )
    title = (
        f"How well do you know {name}? Find out here."
    )
    file_path = path.dirname(path.dirname(__file__))
    file_path = path.join(file_path, 'static', 'data', 'social_icons.json')
    with open(file_path) as f:
        json_data = json.load(f)
    for social, attrs in json_data.items():
        href = attrs['href']  # type: str
        href = href.replace('{url}', link)
        href = href.replace('{body}', body)
        href = href.replace('{title}', title)
        attrs['href'] = href
    return json_data
