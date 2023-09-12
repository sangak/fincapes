from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.utils.translation import gettext as _
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from fincapes.mixins import ContextDataMixin
from ..forms import ProjectModelForm, CommitmentBSModelForm
from ..models import Project, Commitment


class ProjectHomeView(LoginRequiredMixin, ContextDataMixin, UpdateView):
    template_name = 'projects/index.html'
    form_class = ProjectModelForm
    success_url = reverse_lazy('project:index')

    def get_object(self, queryset=None):
        qs = Project.objects.first()
        return qs

    def get_context_data(self, **kwargs):
        request = self.request
        request.session['project'] = self.get_object().uid
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Project Information | ' + context['page_title']
        context['uri'] = 'projects:general-info'
        return context


class CommitmentBSCreateView(BSModalCreateView):
    template_name = 'projects/commitment-create.html'
    success_url = reverse_lazy('project:index')
    form_class = CommitmentBSModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_uid = self.request.session.get('project', None)
        project = Project.objects.filter(uid=project_uid).first()
        kwargs['project'] = project
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('New Donor Commitment')
        return context


class CommitmentBSUpdateView(BSModalUpdateView):
    template_name = 'projects/commitment-create.html'
    form_class = CommitmentBSModelForm
    success_url = reverse_lazy('project:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_uid = self.request.session.get('project', None)
        project = Project.objects.filter(uid=project_uid).first()
        kwargs['project'] = project
        return kwargs

    def get_object(self, queryset=None, *args, **kwargs):
        uid = self.kwargs.get('uid')
        qs = Commitment.objects.filter(uid=uid)
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('Update Donor Commitment')
        return context


class CommitmentBSDeleteView(BSModalDeleteView):
    template_name = 'portal/delete-modal-data.html'
    success_url = reverse_lazy('project:index')
    success_message = _('Commitment is successfully deleted')
    content_name = None

    def get_object(self, queryset=None):
        pk = self.kwargs.pop('pk', None)
        qs = Commitment.objects.filter(pk=pk)
        if qs.exists():
            obj = qs.first()
            self.content_name = obj.donor.title
            return obj
        raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = _('Delete commitment')
        context['content_name'] = self.content_name
        return context