from django.contrib import messages
from django.contrib.auth.views import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalFormView
from fincapes.mixins import ContextNoDataMixin, RequestFormAttachMixin
from ..forms import UserProfileForm, BSUploadAvatarForm
from ..models import Profile

User = get_user_model()


class UpdateProfileView(ContextNoDataMixin, LoginRequiredMixin, UpdateView):
    template_name = 'profile/profile-update.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('account:update-avatar')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Profile Update') + ' | ' + context['page_title']
        context['show_sidebar'] = False
        context['uri'] = 'profile_update'
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class UploadAvatarView(ContextNoDataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile-update.html'
    success_url = reverse_lazy('portal:index')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Update avatar') + ' | ' + context['page_title']
        context['show_sidebar'] = False
        context['uri'] = 'avatar'
        return context


class BSUploadAvatarView(BSModalFormView):
    form_class = BSUploadAvatarForm
    template_name = 'profile/upload-avatar.html'
