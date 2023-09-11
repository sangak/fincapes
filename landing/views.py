from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext as _
from fincapes.mixins import ContextDataMixin, DropNewsletterSubscribesMixin
from contents.models import Content


class HomepageView(ContextDataMixin, DropNewsletterSubscribesMixin, FormView):
    template_name = 'landing/home-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Welcome to ') + context['page_title']
        context['sliders'] = Content.objects.get_sliders()
        context['uri'] = 'homepage'
        return context


class AboutUsView(ContextDataMixin, TemplateView):
    template_name = 'landing/about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('About Us | ') + context['page_title']
        context['uri'] = 'about-us'
        return context