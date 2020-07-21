import re

from django.urls import reverse
import pytest

# TODO: Implement special method for password-reset-confirm


class TestUsersPostMethod:

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('users:login', {}, {},
             'This field is required', 2),
            ('users:register', {}, {},
             'This field is required', 5),
            ('users:password-reset', {}, {},
             'This field is required', 1),
        ]
    )
    def test_users_empty_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        client
    ):
        """ Test clients are unregistered here but should be able to post
        data in these views. The data is empty here and there should be
        <num_expected> instances of <expected_response> in the response
        content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('users:profile-update',
             {'username': 'testuser'}, {},
             'This field is required', 9),
            ('users:password-change', {}, {},
             'This field is required', 3),
        ]
    )
    def test_users_empty_data_registered(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        login_user
    ):
        """ Test clients are registered here and should be able to post
        data in these views. The data is empty here and there should be
        <num_expected> instances of <expected_response> in the response
        content """

        user, client = login_user()
        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

# TODO: Fix all tests underneath

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('users:login', {}, {'username': 'testuser'},
             'This field is required', 1),
            ('users:register', {}, {'password1': 'testpassword'},
             'This field is required', 4),
            ('users:register', {}, {
                'username': 'testuser',
                'last_name': 'testln'
            },
                'This field is required', 3),
            ('users:register', {}, {
                'username': 'testuser', 'first_name': 'testfn',
                'last_name': 'testln'
            },
                'This field is required', 2),
            ('users:register', {}, {
                'first_name': 'testfn',
                'last_name': 'testln',
                'password1': 'testpassword',
                'password2': 'testpassword'
            },
                'This field is required', 1),
        ]
    )
    def test_users_partial_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        client,
    ):
        """ Test clients are unregistered here but should be able to
        post data in these views. The data is partially complete here and
        there should be <num_expected> instances of <expected_response>
        in the response content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn'},
             'This field is required', 8),
            ('users:profile-update', {'username': 'testuser'},
             {'birth_date': '11/11/2001', 'visible': 'off'},
             'This field is required', 7),
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn', 'last_name': 'testln',
              'email': 'test@email.com'},
             'This field is required', 6),
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn', 'last_name': 'testln',
              'email': 'test@email.com', 'birth_date': '11/11/2001'},
             'This field is required', 5),
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn', 'last_name': 'testln',
              'email': 'test@email.com', 'birth_date': '11/11/2001',
              'visible': 'on'},
             'This field is required', 4),
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn', 'last_name': 'testln',
              'email': 'test@email.com', 'birth_date': '11/11/2001',
              'visible': 'on', 'gender': 'male'},
             'This field is required', 3),
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn', 'last_name': 'testln',
              'email': 'test@email.com', 'birth_date': '11/11/2001',
              'visible': 'on', 'gender': 'male', 'country': 'india'},
             'This field is required', 2),
            ('users:profile-update', {'username': 'testuser'},
             {'first_name': 'testfn', 'last_name': 'testln',
              'email': 'test@email.com', 'birth_date': '11/11/2001',
              'visible': 'on', 'gender': 'male', 'country': 'india',
              'recieve_emails': 'on'},
             'This field is required', 2),
            ('users:password-change', {}, {'new_password2': 'new-pass'},
             'This field is required', 2),
            ('users:password-change', {},
             {'new_password1': 'new-pass', 'new_password2': 'new-pass'},
             'This field is required', 1),
        ]
    )
    def test_users_partial_data_registered(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        login_user
    ):
        """ Test clients are registered here and they should be able to
        post data in these views. The data is partially complete here and
        there should be <num_expected> instances of <expected_response> in the
        response content """

        user, client = login_user()
        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('home:contact', {}, {
                'from_email': 'testemail.com', 'message': 'test message body',
                'subject': 'test subject'
            },
                'Enter a valid email', 1),
            ('home:contact', {}, {
                'from_email': 'test@email.com',
                'message': '', 'subject': ''
            },

                'This field is required', 2),
        ]
    )
    def test_users_invalid_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        client
    ):
        """ Test clients are unregistered here but should be able to
        post data in these views. The data is complete here, but
        invalid and there should be <num_expected> instances of
        <expected_response> in the response content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected


@pytest.mark.unittest
class TestInteractionsPostMethodValid:
    """ The data submitted here should be completely valid. Tests
    should not be parameterized here, unless they really need to be. """

    def test_users_pass_reset_email(self, client):
        """ Test clients are unregistered here but should be able to post
        data in these views. The data is complete and valid here and the
        data sent through form should be present in the mail inbox """


if __name__ == '__main__':
    pytest.main()
