from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from .models import Awp
from fincapes.helpers import DatatableView
from projects.models import (
    Project, UltimateOutcome, IntermediateOutcome,
    ImmediateOutcome, Output
)


class AwpAjaxListView(DatatableView):
    model = Awp
    initial_order = []
    column_defs = [
        {'name': 'output', 'title': 'Output', 'foreign_field': 'output__uid', 'visible': True, },
        {'name': 'title', 'title': 'Activity', 'visible': True, 'orderable': True, },
        {'name': 'year', 'title': 'Year', 'visible': False, },
        {'name': 'sub_activity', 'title': 'Sub Activity', 'm2m_foreign_field': 'sub_activity__title', 'visible': True, 'orderable': False}
    ]

    def get_initial_queryset(self, request=None):
        project_uid = request.session.get('project')
        project = Project.objects.filter(uid=project_uid).first()
        ultimate = UltimateOutcome.objects.filter(project=project).first()
        intermediate = IntermediateOutcome.objects.filter(ulti_outcome=ultimate)
        immediate = ImmediateOutcome.objects.filter(inter_outcome__in=intermediate)
        output = Output.objects.filter(imme_outcome__in=immediate).all()
        return Awp.objects.filter(output__in=output).all()


