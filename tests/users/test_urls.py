import pytest
from django.contrib.auth import views as auth_views

from users.views import (
    UserRegistrationView, UserLogoutView,
    ProfileView,
    UserLoginView,
    update_profile_view,
    result_view,
    password_change_view,
    UserPasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    SelfAnswerGroupsListView
)


@pytest.mark.parametrize(
    "reverse_url, kwargs, resolve_url, view_func",
    [
        ('users:register', {}, '/users/handling/register/',
         UserRegistrationView),
        ('users:results', {'username': 'testuser'},
         '/users/results/testuser/', result_view),
        ('users:profile-update',
         {'username': 'testuser'},
         '/users/profile/testuser/update/', update_profile_view),
        ('users:password-change', {}, '/users/password-change/',
         password_change_view),
        ('users:profile', {'username': 'testuser'},
         '/users/profile/testinguser/', ProfileView),
        ('users:login', {}, '/users/handling/login/', UserLoginView),
        ('users:logout', {}, '/users/handling/logout/', UserLogoutView),
        ('users:password-change-done', {}, '/users/password-change/done/',
         UserPasswordChangeDoneView),
        ('users:password-reset', {}, '/users/password-reset/',
         PasswordResetView),
        ('users:password-reset-done', {}, '/users/password-reset/done/',
         PasswordResetDoneView),
        ('users:password-reset-confirm',
         {'uidb64': '27c80dab7a26c5e1', 'token': '27c80dab7a26c5e1'},
         '/users/password-reset/confirm/27c80dab7a26c5e1/27c80dab7a26c5e1/',
         PasswordResetConfirmView),
        ('users:password-reset-complete', {},
         '/users/password-reset/complete/', PasswordResetCompleteView),
        ('users:self-answer-profiles', {'profile_pk': 1},
         '/users/results/self/answers/1/', SelfAnswerGroupsListView),
    ]
)
@pytest.mark.unittest
def test_users_urls(
    reverse_url,
    kwargs,
    resolve_url,
    view_func,
    return_views,
):
    """ Test app-> users urls """

    reverse_view, resolve_view = return_views(reverse_url, resolve_url, kwargs)

    try:
        assert reverse_view.func == view_func
        assert resolve_view.func == view_func
    except (AttributeError, AssertionError):
        assert reverse_view.func.view_class == view_func
        assert resolve_view.func.view_class == view_func


if __name__ == '__main__':
    pytest.main()
