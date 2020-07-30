from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from .forms import ContactForm
from .functions import get_home_context
from core.mixins import GoogleRecaptchaMixin


class HomeView(TemplateView):
    template_name = 'home/home.html'
    extra_context = {'data': get_home_context}


class ResourcesView(TemplateView):
    template_name = 'home/resources.html'


class ContactView(GoogleRecaptchaMixin, FormView):
    template_name = 'home/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home:contact-done')

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)


class ContactDoneView(TemplateView):
    template_name = 'home/contact_done.html'
