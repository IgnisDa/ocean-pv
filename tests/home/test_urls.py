import pytest

from home.views import (
    HomeView,
    ContactView,
    ContactDoneView,
    ResourcesView
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "reverse_url, kwargs, resolve_url, view_func",
    [
        ('home:home', {}, '/', HomeView),
        ('home:contact', {}, '/contact/', ContactView),
        ('home:contact-done', {}, '/contact/done/', ContactDoneView),
        ('home:resources', {}, '/resources/', ResourcesView),
    ]
)
def test_home_urls(
    return_views,
    reverse_url,
    kwargs,
    resolve_url,
    view_func
):
    """ Test app-> home urls """

    reverse_view, resolve_view = return_views(reverse_url, resolve_url, kwargs)

    try:
        assert reverse_view.func == view_func
        assert resolve_view.func == view_func
    except (AttributeError, AssertionError):
        assert reverse_view.func.view_class == view_func
        assert resolve_view.func.view_class == view_func


if __name__ == '__main__':
    pytest.main()
