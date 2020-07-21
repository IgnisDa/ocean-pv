from django.urls import reverse
import pytest


@pytest.mark.unittest
class TestGraphsViewsGetMethod:

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, template_name",
        [
            ('graphs:multiple_results', {}, 'graphs/multiple_results.html'),
        ]
    )
    def test_graphs_views_unregistered(
        self,
        view_namespace_url,
        kwargs,
        template_name,
        login_user
    ):
        """ Test clients are registered here and they should be able to access
        these views. """

        user, client = login_user()
        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.get(url)

        assert response.status_code == 200
        assert template_name in [t.name for t in response.templates]

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, template_name, model",
        [
            ('graphs:single_result', {'pk': 1},
             'graphs/single_result.html', 'SelfAnswerGroup'),
        ]
    )
    @pytest.mark.testing
    def test_graphs_views_registered(
        self,
        view_namespace_url,
        kwargs,
        template_name,
        model,
        login_user,
        create_self_answers,
        create_averages
    ):
        """ Test clients are registered here and they should be able to access 
        these views """

        user, client = login_user()
        answer_group = create_self_answers(user)
        create_averages()
        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.get(url)

        assert response.status_code == 200
        assert template_name in [t.name for t in response.templates]


if __name__ == '__main__':
    pytest.main()
