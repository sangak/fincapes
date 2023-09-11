from django.urls import path
from .views import DetailArticleView

app_name = 'Articles'

urlpatterns = [
    path('<slug>&id=<pk>/', DetailArticleView.as_view(), name='detail'),
]