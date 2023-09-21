from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.http import JsonResponse
from multi_form_view.base import MultiModelFormView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from fincapes.mixins import ContextDataMixin, PreviousUrlMixin
from .models import Awp, SubActivity
from projects.models import Project, Output
from .forms import AwpBSModelForm


class AwpHomeView(LoginRequiredMixin, ContextDataMixin, PreviousUrlMixin, TemplateView):
    template_name = 'awp/home-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Annual Work Plan') + ' | ' + context['page_title']
        context['uri'] = 'projects:awp'
        context['prev_path'] = self.get_prev_url()
        context['project'] = Project.objects.first()
        return context


class AwpByYearView(LoginRequiredMixin, ContextDataMixin, PreviousUrlMixin, TemplateView):
    template_name = 'awp/by-year.html'

    # @staticmethod
    def get_year_active(self):
        year = self.kwargs.get('year', None)
        return year

    def get_context_data(self, **kwargs):
        request = self.request
        year = self.get_year_active()
        request.session['awp_year'] = year
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{year} {_('Annual Work Plan')} | {context['page_title']}"
        context['uri'] = 'projects:awp'
        context['year'] = year
        context['prev_path'] = request.session.get('previous_url')
        return context


class AwpBSCreateView(LoginRequiredMixin, BSModalCreateView, MultiModelFormView):
    template_name = 'awp/add-activity.html'
    success_url = reverse_lazy('awp:index')
    form_classes = {
        'form': AwpBSModelForm
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('New Activity')
        return context


def storenum_from_output(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST' and request.is_ajax:
            output_pk = request.POST.get('output')
            qs = Output.objects.filter(pk=output_pk)
            if qs.exists():
                obj = qs.first()
                new_num = Awp.objects.new_num(obj)
    data = {
        'message': f'{obj.code}.{new_num}'
    }
    return JsonResponse(data, safe=False)