from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from fincapes.mixins import ContextDataMixin
from .models import Donor
from .forms import DonorBSModelForm


class DonorHomeView(LoginRequiredMixin, ContextDataMixin, TemplateView):
    template_name = 'donors/donor-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Donor Information | ' + context['page_title']
        context['uri'] = 'donors'
        context['donors'] = Donor.objects.all()
        return context


class DonorBSCreateView(BSModalCreateView):
    template_name = 'donors/donor-create.html'
    form_class = DonorBSModelForm
    success_url = reverse_lazy('donor:index')
    success_message = 'Success: Donor was created.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['created'] = True
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('Create Donor')
        return context


class DonorBSUpdateView(BSModalUpdateView):
    template_name = 'donors/donor-create.html'
    form_class = DonorBSModelForm
    success_url = reverse_lazy('donor:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['created'] = False
        return kwargs

    def get_object(self, queryset=None, *args, **kwargs):
        uid = self.kwargs.get('uid')
        qs = Donor.objects.filter(uid=uid)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('Edit Donor')
        return context


class DonorBSDeleteView(BSModalDeleteView):
    template_name = 'portal/delete-modal-data.html'
    success_message = _('Donor is successfully deleted')
    success_url = reverse_lazy('donor:index')
    model = Donor

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        qs = Donor.objects.filter(pk=pk).first()
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('Delete donor')
        context['content_name'] = qs
        return context

