from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, auth_logout, get_user_model
from django.utils.translation import get_language, gettext as _
from django.views.generic import CreateView, View, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from fincapes.helpers import remove_session
from fincapes.mixins import (
    NextUrlMixin, RequestFormAttachMixin, ContextNoDataMixin
)
from ..forms import LoginForm, RegistrationForm
from fincapes.variables import aplikasi

User = get_user_model()


class LoginRequestView(ContextNoDataMixin, NextUrlMixin, LoginView):
    template_name = 'accounts/login-register.html'
    default_next = reverse_lazy('portal:index')
    success_url = reverse_lazy('portal:index')
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login | ' + context['page_title']
        context['uri'] = 'login'
        context['show_sidebar'] = False
        return context

    def form_valid(self, form):
        next_path = self.get_next_url()
        print(next_path)
        user = self.request.user
        if user.invited_user:
            if not user.has_change_password:
                pass
        if not user.is_profile_filled:
            return HttpResponseRedirect(reverse_lazy('account:update'))
        return redirect(next_path)


class RegistrationView(ContextNoDataMixin, CreateView):
    template_name = 'accounts/login-register.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Register | ' + context['page_title']
        context['uri'] = 'register'
        context['show_sidebar'] = False
        return context


class LogoutRequestView(NextUrlMixin, RequestFormAttachMixin, View):
    default_next = reverse_lazy('login')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        try:
            auth_logout(request)
        except KeyError as error:
            messages.error(request, error.message)
            pass

        next_path = self.get_next_url()
        if next_path:
            return HttpResponseRedirect(next_path)
        return super().dispatch(request, *args, **kwargs)