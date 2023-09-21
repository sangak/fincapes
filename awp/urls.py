from django.urls import path
from .datatables import AwpAjaxListView
from .views import (
    AwpHomeView, AwpBSCreateView, AwpByYearView, storenum_from_output
)

app_name = 'Awp'

urlpatterns = [
    path('', AwpHomeView.as_view(), name='index'),
    path('create/', AwpBSCreateView.as_view(), name='create'),
    path('<str:year>/', AwpByYearView.as_view(), name='by_year'),
    path('by-year/list-ajax/', AwpAjaxListView.as_view(), name='awp-ajax-list'),
    path('new-store/', storenum_from_output, name='store-num-by-output'),
]