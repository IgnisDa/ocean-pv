from django.urls import path

from . import views

app_name = 'graphs'

urlpatterns = [
    path('test/', views.MultipleResultView.as_view(),
         name='test'),
    path('single/<int:pk>/', views.IndividualResultView.as_view(),
         name='single_result'),
    path('comparison/<int:self_pk>/<int:relation_pk>/',
         views.ComparisonResultView.as_view(), name='comparison_view'),
    path('multiple/', views.multiple_result_view, name='multiple_results'),
    path('update-accuracy/', views.update_accuracy, name='update-accuracy'),
]
