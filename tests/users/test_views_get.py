import re

from django.urls import reverse
import pytest


@pytest.mark.unittest
class TestUsersViewsGetMethod:

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, template_name",
        [
            ('users:profile', {'username': 'testinguser'},
             'users/profile.html'),
            ('users:results', {'username': 'testinguser'},
             'users/results.html'),
            ('users:profile-update',
             {'username': 'testinguser'}, 'users/user profile_form.html'),

            ('users:password-change', {}, 'users/password_change_form.html'),
            ('users:password-change-done', {},
             'users/password_change_done.html'),
            ('users:self-answer-profiles', {'profile_pk': 1},
             'users/selfanswergroup_choice_view.html'),
        ]
    )
    def test_users_views_unregistered(
        self,
        view_namespace_url,
        kwargs,
        template_name,
        client
    ):
        """ Test clients are unregistered here and shouldn't be able to
        access these views """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.get(url)

        assert response.status_code == 302
        assert template_name not in [t.name for t in response.templates]

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, template_name",
        [
            ('users:login', {}, 'users/login.html'),
            ('users:logout', {}, 'users/logout.html'),
            ('users:register', {}, 'users/register.html'),

            ('users:password-reset', {},
             'users/password_reset/password_reset_form.html'),
            ('users:password-reset-done', {},
             'users/password_reset/password_reset_done.html'),
            ('users:password-reset-confirm',
             {'token': 'uMMOt9DTk3L9ETVt7gDjkJXzZ3P7KKAKdYViuyJQmWE',
              'uidb64': 'X2k'},
             'users/password_reset/password_reset_confirm.html'),
            ('users:password-reset-complete', {},
             'users/password_reset/password_reset_complete.html'),
        ]
    )
    def test_users_views(
        self,
        view_namespace_url,
        kwargs,
        template_name,
        client
    ):
        """ Test clients are unregistered here but should be able to access 
        these views """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.get(url)

        assert response.status_code == 200
        assert template_name in [t.name for t in response.templates]

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, template_name",
        [
            ('users:profile', {'username': 'testinguser'},
             'users/profile.html'),
            ('users:results', {'username': 'testinguser'},
             'users/results.html'),
            ('users:profile-update',
             {'username': 'testinguser'}, 'users/userprofile_form.html'),
            ('users:password-change', {}, 'users/password_change_form.html'),
            ('users:password-change-done', {},
             'users/password_change_done.html'),
            ('users:self-answer-profiles', {'profile_pk': 1},
             'users/selfanswergroup_choice_view.html')

        ]
    )
    def test_users_views_registered(
        self,
        view_namespace_url,
        kwargs,
        template_name,
        login_user,
    ):
        """ Test clients are registered here and they should be able to 
        access these views """

        user, client = login_user()
        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.get(url)

        assert response.status_code == 200
        assert template_name in [t.name for t in response.templates]


if __name__ == '__main__':
    pytest.main()
