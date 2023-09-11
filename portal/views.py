import pendulum
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from fincapes.mixins import (
    NextUrlMixin, PreviousUrlMixin, ContextDataMixin
)
from fincapes.variables import aplikasi


class HomeDashboardView(PreviousUrlMixin, NextUrlMixin, LoginRequiredMixin, ContextDataMixin, TemplateView):
    template_name = 'portal/dashboard.html'
    month = None

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dashboard | ' + context['page_title']
        context['uri'] = 'portal'
        context['prev_url'] = self.get_prev_url()
        return context


@csrf_exempt
def no_response(request):
    data = dict()
    data['response'] = None
    return JsonResponse(data, safe=False)