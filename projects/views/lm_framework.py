from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from fincapes.mixins import ContextDataMixin


class LogicModelHomeView(LoginRequiredMixin, ContextDataMixin, TemplateView):
    template_name = 'logic_model/home-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Logic Model | ' + context['page_title']
        context['uri'] = 'projects:logic-model'
        return context