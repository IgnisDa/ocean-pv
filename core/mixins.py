from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """ The LoginRequiredMixin extended to add a relevant message to the
    messages framework by setting the ``permission_denied_message``
    attribute. """

    permission_denied_message = 'You have to be logged in to access that page'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class RequiredFieldsMixin:
    """ This can be used as a mixin in forms to easily specify which fields
    are required through the ``required_fields`` attribute, in the ``Meta``
    class. Excluded fields are not touched. """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        required_fields = getattr(self.Meta, 'required_fields', None)

        if required_fields:
            if required_fields == '__all__':
                for key in self.fields:
                    self.fields[key].required = True
            for key in self.fields:
                if key in required_fields:
                    self.fields[key].required = True
