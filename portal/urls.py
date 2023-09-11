from django.urls import path
from .views import HomeDashboardView, no_response

app_name = 'Portal'

urlpatterns = [
    path('', HomeDashboardView.as_view(), name='index'),
    path('no-response/', no_response, name='no_response')
]