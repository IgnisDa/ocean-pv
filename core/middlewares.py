from django.http import HttpRequest
from django.shortcuts import redirect, reverse
from django.contrib import messages

from users.models import UserProfile


class ReferralCheckMiddleware(object):
    """ This middleware checks if the following instances are set, and if
    they are, it means that the request user has accessed the website using
    a referral link and should be treated accordingly. They are redirected to
    ``users:referral-new``. The instances are:

        1) request.session['profile_pk']
        2) request.session['against']

    If these instances have been set, it is assumed that the user has accessed
    the website using a referral link.

    NOTE: No longer used due to its complexity.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(
        self, request: HttpRequest,
        view_func, view_args, view_kwargs
    ):
        profile_pk = request.session.get('profile_pk', False)
        against = request.session.get('against', False)  # some func
        handling = request.session.get('handling', False)
        if (profile_pk and against):
            url = request.get_full_path()
            if url == self.login_url or url == self.register_url:
                request.session['handling'] = True
                if handling is True and url == self.login_url:
                    test_url = reverse(
                        'interactions:taketest-relations',
                        kwargs={'profile_pk': profile_pk, 'against': against}
                    )
                    try:
                        request.session.pop('profile_pk')
                        request.session.pop('against')
                        request.session.pop('signup')
                    except KeyError:
                        pass
                    return redirect(test_url)


class ProfileCompletionCheckMiddleware:
    # TODO: Add docstring
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(
        self, request: HttpRequest,
        view_func, view_args, view_kwargs
    ):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
        else:
            return None
        link = reverse('users:profile-update',
                       kwargs={'username': request.user.username})
        if not user_profile.user.email:
            messages.success(
                request,
                "Looks like you haven't completed your profile. Complete "
                f"it <a href='{link}' class='text-success'>here</a> for a "
                "more tailored experience"
            )
        return None
