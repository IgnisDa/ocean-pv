from django.urls import path, include
from . import views

app_name = 'interactions'


extra_urls_howto = [
    path('referral/', views.ReferralView.as_view(), name='howto-referral'),
    path('', views.HowtoView.as_view(), name='howto'),
    path('ajax/', views.howto_relation_ajax, name='howto-relations-ajax'),
    path('random-user/', views.random_user_view, name='random-user'),
    path('relations/', views.howto_relations_view, name='howto-relations')
]

extra_urls_taketest = [
    path('', views.SelfQuestionView.as_view(), name='taketest'),
    path('relations/<int:profile_pk>/<int:against>/',
         views.RelationQuestionView.as_view(), name='taketest-relations'),

]

urlpatterns = [
    path('howto/', include(extra_urls_howto)),
    path('taketest/', include(extra_urls_taketest)),
    path('view/', views.View.as_view(), name='view')
]
