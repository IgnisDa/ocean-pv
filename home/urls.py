from django.urls import path, include
from . import views

app_name = 'home'

extra_url_contact = [
    path('', views.ContactView.as_view(), name='contact'),
    path('done/', views.ContactDoneView.as_view(), name='contact-done'),
]
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('resources/', views.ResourcesView.as_view(), name='resources'),
    path('contact/', include(extra_url_contact)),
]
