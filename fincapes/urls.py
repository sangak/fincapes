"""fcapes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import LoginRequestView, RegistrationView, LogoutRequestView

urlpatterns = [
    path('', include('landing.urls', namespace='frontpage')),
    path('account/', include('accounts.urls', namespace='account')),
    path('article/', include('articles.urls', namespace='article')),
    path('awp/', include('awp.urls', namespace='awp')),
    path('donors/', include('donors.urls', namespace='donor')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('portal/', include('portal.urls', namespace='portal')),
    path('project/', include('projects.urls', namespace='project')),
    path("select2/", include("django_select2.urls")),
    path('settings/admin/', admin.site.urls),
    path('user/auth/', LoginRequestView.as_view(), name='login'),
    path('user/register/', RegistrationView.as_view(), name='register'),
    path('user/sign-out/', LogoutRequestView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)