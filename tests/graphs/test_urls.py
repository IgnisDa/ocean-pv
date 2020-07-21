import pytest
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from graphs.views import (
    IndividualResultView,
    multiple_result_view
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "reverse_url, kwargs, resolve_url, view_func",
    [
        ('graphs:multiple_results', {},
         '/graphs/multiple/', multiple_result_view),
        ('graphs:single_result', {'pk': 30},
         '/graphs/single/30/', IndividualResultView),
    ]
)
def test_home_urls(
    return_views,
    reverse_url,
    kwargs,
    resolve_url,
    view_func,
    create_averages
):
    """ Test app-> graphs urls """

    create_averages()
    reverse_view, resolve_view = return_views(
        reverse_url, resolve_url, kwargs
    )

    try:
        assert reverse_view.func == view_func
        assert resolve_view.func == view_func
    except (AttributeError, AssertionError):
        assert reverse_view.func.view_class == view_func
        assert resolve_view.func.view_class == view_func


if __name__ == '__main__':
    pytest.main()
