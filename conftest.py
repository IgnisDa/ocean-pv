import pytest
from django.urls import resolve, reverse


@pytest.fixture
def test_password():
    """ Returns a test password for user login. """

    return 'test-pass'


@pytest.fixture()
def test_username():
    """ Returns a test username for user login. """

    return "testinguser"


@pytest.fixture()
def create_user(test_username, test_password, django_user_model):
    """ Creates a test ``user`` which can be used to login. """

    def _create_user(**kwargs):
        if 'username' not in kwargs:
            kwargs['username'] = test_username
        if 'password' not in kwargs:
            kwargs['password'] = test_password
        return django_user_model.objects.create_user(**kwargs)

    return _create_user


@pytest.fixture()
def login_user(create_user, test_password, client):
    """ Logs in a user with their correct password and returns ``client`` and
    ``user``. """

    def _login_user(user=None, password=None):
        if user is None:
            user = create_user()
            password = test_password
        client.login(
            username=user.username,
            password=password
        )
        return user, client

    return _login_user


@pytest.fixture
def return_views():
    """ Returns the view using ``reverse_url`` and corresponding
    ``kwargs`` (if any). """

    def _return_views(reverse_url, resolve_url, kwargs):
        reverse_view = resolve(reverse(reverse_url,
                                       kwargs=kwargs if kwargs else None))
        resolve_view = resolve(resolve_url)

        return reverse_view, resolve_view

    return _return_views
