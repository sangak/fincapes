from django.urls import path
from .views import HomeDashboardView, no_response, check_session, storenum_from_output

app_name = 'Portal'

urlpatterns = [
    path('', HomeDashboardView.as_view(), name='index'),
    path('session-check/', check_session, name='session-check'),
    path('no-response/', no_response, name='no_response'),
    path('store-num/', storenum_from_output, name='store-num'),
]