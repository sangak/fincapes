from django.urls import path
from . import views, datatables

app_name = 'Project'

urlpatterns = [
    path('', views.ProjectHomeView.as_view(), name='index'),
    path('commitment-ajax-list/', datatables.CommitmentAjaxListView.as_view(), name='commitment-ajax-list'),
    path('new-commitment/', views.CommitmentBSCreateView.as_view(), name='new-commitment'),
    path('commitment-update/<uid>/', views.CommitmentBSUpdateView.as_view(), name='update-commitment'),
    path('commitment-delete/<pk>/', views.CommitmentBSDeleteView.as_view(), name='delete-commitment'),
    path('logic-model/', views.LogicModelHomeView.as_view(), name='logic-model-index'),
    path('logic-model/ultimate/<uid>/', views.UltimateBSUpdateView.as_view(), name='update-ultimate'),
    path('logic-model/intermediate/<uid>/', views.IntermediateBSUpdateView.as_view(), name='update-intermediate'),
    path('logic-model/immediate/<uid>/', views.ImmediateBSUpdateView.as_view(), name='update-immediate'),
    path('logic-model/output/<uid>/', views.OutputBSUpdateView.as_view(), name='update-output'),
    path('logic-model/update-ultimate-ajax/<uid>/', views.ultimate_response, name='update-ajax-ultimate'),
    path('logic-model/update-intermediate-ajax/<uid>/', views.intermediate_response, name='update-ajax-intermediate'),
    path('logic-model/update-immediate-ajax/<uid>/', views.immediate_response, name='update-ajax-immediate'),
    path('logic-model/update-output-ajax/<uid>/', views.output_response, name='update-ajax-output')
]