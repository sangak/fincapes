from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from multi_form_view.base import MultiModelFormView
from fincapes.mixins import ContextDataMixin, PreviousUrlMixin, ContextNoDataMixin, AddAnimationMixin
from ..models import UltimateOutcome
from ..forms import ProjectModelForm, UltimateOutcomeForm


class LogicModelHomeView(LoginRequiredMixin, ContextDataMixin, PreviousUrlMixin, TemplateView):
    template_name = 'logic_model/home-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Logic Model | ' + context['page_title']
        context['uri'] = 'projects:logic-model'
        context['prev_path'] = self.get_prev_url()
        return context


class AddLogicModelView(LoginRequiredMixin, ContextNoDataMixin, AddAnimationMixin, MultiModelFormView):
    template_name = 'logic_model/add-logic.html'
    prev_url = None
    form_classes = {
        'ultimate': UltimateOutcomeForm
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Logic Model | ' + context['page_title']
        context['page_sub_title'] = _('Add Logic Model')
        context['show_sidebar'] = False
        context['css_id'] = 'add-animation'
        context['uri'] = 'add_ultimate'
        return context