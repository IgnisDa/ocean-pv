from django.urls import reverse, resolve
import pytest

from interactions.views import (
    HowtoView,
    View,
    SelfQuestionView,
    RelationQuestionView,
    howto_relations_view
)


@pytest.mark.unittest
@pytest.mark.parametrize(
    "reverse_url,kwargs ,resolve_url, view_func",
    [
        # Func-based Views
        ('interactions:taketest', {}, '/interactions/taketest/',
         SelfQuestionView),
        ('interactions:taketest-relations',
         {'profile_pk': 1, 'against': 12},
         '/interactions/taketest/relations/1/12/', RelationQuestionView),

        # Class-based Views
        ('interactions:howto', {}, '/interactions/howto/', HowtoView),
        ('interactions:howto-relations', {},
         '/interactions/howto/relations/', howto_relations_view),
        ('interactions:view', {}, '/interactions/view/', View),
    ]
)
def test_urls_interactions(
    return_views,
    kwargs,
    reverse_url,
    resolve_url,
    view_func
):
    """ Test app-> interactions urls """

    reverse_view, resolve_view = return_views(reverse_url, resolve_url, kwargs)

    try:
        assert reverse_view.func == view_func
        assert resolve_view.func == view_func
    except (AttributeError, AssertionError):
        assert reverse_view.func.view_class == view_func
        assert resolve_view.func.view_class == view_func


if __name__ == '__main__':
    pytest.main()
