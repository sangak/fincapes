from django.urls import path
from . import views, datatables

app_name = 'Donor'

urlpatterns = [
    path('', views.DonorHomeView.as_view(), name='index'),
    path('create/', views.DonorBSCreateView.as_view(), name='create'),
    path('delete/<pk>/', views.DonorBSDeleteView.as_view(), name='delete'),
    path('donor-list/', datatables.DonorAjaxListView.as_view(), name='donor-list-ajax'),
    path('update/<str:uid>/', views.DonorBSUpdateView.as_view(), name='update')
]