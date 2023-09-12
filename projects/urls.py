from django.urls import path
from . import views, datatables

app_name = 'Project'

urlpatterns = [
    path('', views.ProjectHomeView.as_view(), name='index'),
    path('commitment-ajax-list/', datatables.CommitmentAjaxListView.as_view(), name='commitment-ajax-list'),
    path('new-commitment/', views.CommitmentBSCreateView.as_view(), name='new-commitment'),
    path('commitment-update/<uid>/', views.CommitmentBSUpdateView.as_view(), name='update-commitment'),
    path('commitment-delete/<pk>/', views.CommitmentBSDeleteView.as_view(), name='delete-commitment'),
    path('logic-model/', views.LogicModelHomeView.as_view(), name='logic-model-index')
]