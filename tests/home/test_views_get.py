import re

from django.urls import resolve, reverse
from django.core import mail
from django.conf import settings
import pytest


@pytest.mark.unittest
class TestHomeGetMethod:

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, template_name",
        [
            ('home:home', {}, 'home/home.html'),
            ('home:contact-done', {}, 'home/contact_done.html'),
            ('home:contact', {}, 'home/contact.html'),
            ('home:resources', {}, 'home/resources.html')
        ]
    )
    @pytest.mark.django_db
    def test_home_views(
        self,
        view_namespace_url,
        kwargs,
        template_name,
        client
    ):
        """ Test clients are unregistered here but should be able to access these views """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.get(url)

        assert response.status_code == 200
        assert template_name in [t.name for t in response.templates]


class TestHomePostMethod:

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('home:contact', {}, {}, 'This field is required', 3),
        ]
    )
    def test_home_empty_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        client
    ):
        """ Test clients are unregistered here but should be able to post data in these views. The data is empty here and there should be <num_expected> instances of <expected_response> in the response content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('home:contact', {}, {'from_email': 'testemail@email.com'},
             'This field is required', 2),
            ('home:contact', {}, {'subject': 'test subject'},
             'This field is required', 2),
            ('home:contact', {}, {'message': 'test message body'},
             'This field is required', 2),
            ('home:contact', {}, {'from_email': 'testemail@email.com',
                                  'message': 'test message body'}, 'This field is required', 1),
        ]
    )
    def test_home_partial_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        client
    ):
        """ Test clients are unregistered here but should be able to post data in these views. The data is partially complete here and there should be <num_expected> instances of <expected_response> in the response content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response, num_expected",
        [
            ('home:contact', {}, {'from_email': 'testemail.com', 'message': 'test message body', 'subject': 'test subject'},
             'Enter a valid email', 1),
            ('home:contact', {}, {'from_email': 'test@email.com', 'message': '', 'subject': ''},
             'This field is required', 2),
        ]
    )
    def test_home_invalid_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        num_expected,
        client
    ):
        """ Test clients are unregistered here but should be able to post data in these views. The data is complete here, but invalid and there should be <num_expected> instances of <expected_response> in the response content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert len(list(re.finditer(expected_response,
                                    response_content))) is num_expected

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data, expected_response",
        [
            ('home:contact', {}, {'from_email': 'test@email.com', 'message': 'This is a test message', 'subject': 'This is a test body'},
             'Your contact form has been submitted'),
        ]
    )
    def test_home_valid_data(
        self,
        view_namespace_url,
        kwargs,
        data,
        expected_response,
        client
    ):
        """ Test clients are unregistered here but should be able to post data in these views. The data is complete and valid here and there should be instances of <expected_response> in the response content """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data, follow=True)
        response_content = response.content.decode()

        assert response.status_code == 200
        assert expected_response in response_content

    @pytest.mark.parametrize(
        "view_namespace_url, kwargs, data",
        [
            ('home:contact', {}, {'from_email': 'test@email.com',
                                  'message': 'This is a test message', 'subject': 'This is a test subject'}),
        ]
    )
    def test_home_contact_email(
        self,
        view_namespace_url,
        kwargs,
        data,
        client
    ):
        """ Test clients are unregistered here but should be able to post data in these views. The data is complete and valid here and there should be the data sent through form should be present in the mail inbox """

        url = reverse(view_namespace_url, kwargs=kwargs if kwargs else None)
        response = client.post(url, data=data, follow=True)

        assert response.status_code == 200
        assert len(mail.outbox) == 1, "Inbox is not empty"
        assert mail.outbox[0].subject == data['subject']
        assert mail.outbox[0].body == data['message']
        assert mail.outbox[0].from_email == data['from_email']
        assert mail.outbox[0].to == [settings.EMAIL_HOST_USER] if settings.EMAIL_HOST_USER else [
            'ocean-pv_dev@email.com']


if __name__ == '__main__':
    pytest.main()
