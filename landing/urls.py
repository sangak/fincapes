from django.urls import path
from .views import HomepageView, AboutUsView

app_name = 'Frontpage'

urlpatterns = [
    path('', HomepageView.as_view(), name='index'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
]