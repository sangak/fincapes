from django.contrib import messages
from django.utils.translation import get_language, gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.validators import URLValidator
from django.http import JsonResponse
from fincapes.variables import aplikasi
from landing.forms import ChangeLanguageForm, NewspaperSubscribeForm
from subscribers.models import Subscriber


class ContextDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = aplikasi
        context['page_title'] = aplikasi.get('portal_app')
        context['language_form'] = ChangeLanguageForm(bahasa=get_language())
        context['show_sidebar'] = True
        context['navbar_needed'] = True
        context['show_footer'] = True
        return context


class ContextNoDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = aplikasi
        context['page_title'] = aplikasi.get('portal_app')
        context['show_sidebar'] = True
        context['navbar_needed'] = True
        context['show_footer'] = True
        return context


class DropNewsletterSubscribesMixin(object):
    form_class = NewspaperSubscribeForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribe_form'] = NewspaperSubscribeForm()
        return context

    def form_valid(self, form):
        full_name = form.cleaned_data.get('full_name')
        email = form.cleaned_data.get('email')
        qs = Subscriber.objects.filter(subscriber_types__contains='newsletter').filter(email=email)
        if not qs.exists():
            form.save()
            messages.success(
                self.request,
                _(
                    '<strong>Hi {}</strong>, <br>Thank you for interesting to know our update information'.format(
                        full_name
                    )
                )
            )
        return super().form_valid(form)


class RequestFormAttachMixin(object):
    def get_from_kwargs(self):
        kwargs = super().get_from_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PreviousUrlMixin(object):
    default_prev = '/'

    def get_prev_url(self):
        request = self.request
        self.default_prev = request.path
        # if not 'previous_url' in request.session:
        #     request.session['previous_url'] = [self.default_prev]
        # else:
        #     request.session['previous_url'] += [self.default_prev]
        request.session['previous_url'] = self.default_prev
        request.session['is_action_done'] = False
        return self.default_prev


class AddAnimationMixin(object):
    prev_url = None
    add_animation = False

    def get_context_data(self, **kwargs):
        request = self.request
        if 'previous_url' in request.session:
            self.prev_url = self.request.session['previous_url']
            if not request.session['is_action_done']:
                self.add_animation = True
                request.session['is_action_done'] = True
        context = super().get_context_data(**kwargs)
        context['add_animation'] = self.add_animation
        context['prev_path'] = self.prev_url
        return context


class NextUrlMixin(object):
    default_next = '/'

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next


class JsonableResponseMixin(object):
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, code=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'response': 'succeed'
            }
            return JsonResponse(data, code=200)


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OptionalURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
            super().__call__(value)