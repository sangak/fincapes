from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.http import JsonResponse
from bootstrap_modal_forms.generic import BSModalUpdateView
from django.views.decorators.csrf import csrf_exempt
from fincapes.mixins import ContextDataMixin, PreviousUrlMixin, ContextNoDataMixin, AddAnimationMixin
from ..models import UltimateOutcome, IntermediateOutcome, ImmediateOutcome, Output
from ..forms import (
    ProjectModelForm, UltimateBSOutcomeForm, IntermediateBSOutcomeForm,
    ImmediateBSOutcomeForm, OutputBSForm
)


class LogicModelHomeView(LoginRequiredMixin, ContextDataMixin, PreviousUrlMixin, TemplateView):
    template_name = 'logic_model/home-index.html'

    @staticmethod
    def get_ultimate():
        ultimate = UltimateOutcome.objects.first()
        return ultimate

    @staticmethod
    def get_intermediate():
        inter = IntermediateOutcome.objects.all()
        return inter

    @staticmethod
    def get_immediate():
        imme = ImmediateOutcome.objects.all()
        return imme

    @staticmethod
    def get_outputs():
        outputs = Output.objects.all()
        return outputs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Logic Model | ' + context['page_title']
        context['uri'] = 'projects:logic-model'
        context['prev_path'] = self.get_prev_url()
        context['ultimate'] = self.get_ultimate()
        context['intermediate'] = self.get_intermediate()
        context['immediate'] = self.get_immediate()
        context['outputs'] = self.get_outputs()
        return context


class UltimateBSUpdateView(LoginRequiredMixin, BSModalUpdateView):
    template_name = 'projects/commitment-create.html'
    form_class = UltimateBSOutcomeForm
    success_url = reverse_lazy('project:logic-model-index')

    def get_object(self, queryset=None):
        uid = self.kwargs.get('uid', None)
        qs = UltimateOutcome.objects.filter(uid=uid)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = 'Ultimate Outcome'
        return context


@csrf_exempt
def ultimate_response(request, uid):
    data = dict()
    if request.method == 'GET':
        qs = UltimateOutcome.objects.filter(uid=uid)
        if qs.exists():
            obj = qs.first()
            data['response'] = obj.description
    return JsonResponse(data)


class IntermediateBSUpdateView(LoginRequiredMixin, BSModalUpdateView):
    template_name = 'projects/commitment-create.html'
    form_class = IntermediateBSOutcomeForm
    success_url = reverse_lazy('project:logic-model-index')

    def get_object(self, queryset=None):
        uid = self.kwargs.get('uid', None)
        qs = IntermediateOutcome.objects.filter(uid=uid)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = 'Intermediate Outcome'
        return context


@csrf_exempt
def intermediate_response(request, uid):
    data = dict()
    if request.method == 'GET':
        qs = IntermediateOutcome.objects.filter(uid=uid)
        if qs.exists():
            obj = qs.first()
            data['response'] = obj.description
    return JsonResponse(data)


class ImmediateBSUpdateView(LoginRequiredMixin, BSModalUpdateView):
    template_name = 'projects/commitment-create.html'
    form_class = ImmediateBSOutcomeForm
    success_url = reverse_lazy('project:logic-model-index')

    def get_object(self, queryset=None):
        uid = self.kwargs.pop('uid', None)
        qs = ImmediateOutcome.objects.filter(uid=uid)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = 'Immediate Outcome'
        return context


@csrf_exempt
def immediate_response(request, uid):
    data = dict()
    if request.method == 'GET':
        qs = ImmediateOutcome.objects.filter(uid=uid)
        if qs.exists():
            obj = qs.first()
            data['response'] = obj.description
    return JsonResponse(data)


class OutputBSUpdateView(LoginRequiredMixin, BSModalUpdateView):
    template_name = 'projects/commitment-create.html'
    form_class = OutputBSForm
    success_url = reverse_lazy('project:logic-model-index')

    def get_object(self, queryset=None):
        uid = self.kwargs.pop('uid', None)
        qs = Output.objects.filter(uid=uid)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = 'Outputs'
        return context


@csrf_exempt
def output_response(request, uid):
    data = dict()
    if request.method == 'GET':
        qs = Output.objects.filter(uid=uid)
        if qs.exists():
            obj = qs.first()
            data['response'] = obj.description
    return JsonResponse(data)