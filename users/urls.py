from django.urls import path, include

from . import views


app_name = 'users'


extra_urls_referral = [
    path('new/<int:profile_pk>/<int:against>/',
         views.referral_view, name='referral-new'),
    path('instructions/',
         views.ReferralInstructionsView.as_view(),
         name='referral-instructions')
]
extra_urls_profile = [
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/update/',
         views.update_profile_view, name='profile-update'),
]
extra_urls_list = [
    path('self/<int:profile_pk>/',
         views.UserSelfAnswerGroupsListView.as_view(), name='list-self'),
    path(
        'relation/<int:profile_pk>/',
        views.UserRelationAnswerGroupsListView.as_view(), name='list-relation'
    ),
    path('others/<int:profile_pk>/',
         views.UserOthersAnswerGroupsListView.as_view(), name='list-other'),
]
extra_urls_results = [
    path('<str:username>/', views.result_view, name='results'),
    path('self/answers/<int:profile_pk>/', views.SelfAnswerGroupsListView.as_view(),
         name='self-answer-profiles'),

    path('list/', include(extra_urls_list)),
]
extra_urls_handling = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
]
extra_urls_password_reset = [
    path('', views.PasswordResetView.as_view(), name='password-reset'),
    path('done/', views.PasswordResetDoneView.as_view(),
         name='password-reset-done'),
    path('confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('complete/', views.PasswordResetCompleteView.as_view(),
         name='password-reset-complete'),
]
extra_urls_password_change = [
    path('', views.password_change_view, name='password-change'),
    path('done/', views.UserPasswordChangeDoneView.as_view(),
         name='password-change-done'), ]

urlpatterns = [
    path('handling/', include(extra_urls_handling)),
    path('profile/', include(extra_urls_profile)),
    path('results/', include(extra_urls_results)),
    path('password-change/', include(extra_urls_password_change)),
    path('password-reset/', include(extra_urls_password_reset)),
    path('referral/', include(extra_urls_referral)),
]
