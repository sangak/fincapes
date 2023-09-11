from django.urls import path
from django.views.generic import RedirectView
from .views import (
    UpdateProfileView, UploadAvatarView, BSUploadAvatarView
)

app_name = 'Account'

urlpatterns = [
    path('', RedirectView.as_view(url='/account/profile-update/'), name='index'),
    path('profile-update/', UpdateProfileView.as_view(), name='update'),
    path('profile-update/avatar/', UploadAvatarView.as_view(), name='update-avatar'),
    path('profile-update/avatar/update/', BSUploadAvatarView.as_view(), name='upload-avatar')
]