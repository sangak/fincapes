from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from .models import Commitment
from fincapes.helpers import DatatableView
from fincapes.utils import currency


class CommitmentAjaxListView(DatatableView):
    model = Commitment
    title = _('Donor Commitment')
    initial_order = []

    column_defs = [
        {'name': 'title', 'title': _('Donor'), 'foreign_field': 'donor__title', 'searchable': True, 'visible': True, "width": "45%", },
        {'name': 'acronym', 'title': _('Acronym'), 'foreign_field': 'donor__acronym', 'searchable': True, 'visible': True, },
        {'name': 'currency', 'title': _('Currency'), 'searchable': True, 'visible': False, },
        {'name': 'amount', 'title': _('Amount'), 'searchable': True, 'visible': True, },
        {'name': 'actions', 'title': "", "orderable": False, "width": "10%", 'searchable': False, }
    ]

    def get_initial_queryset(self, request=None):
        parent_uid = request.session.get('project')
        return Commitment.objects.filter(project__uid=parent_uid).all()

    def customize_row(self, row, obj):
        amount = currency(obj.amount)
        total = f'''
        <div class="d-flex flex-row justify-content-between">
            <div class="text-start">
                <span>{obj.get_currency_display()}</span>
            </div>
            <div class="text-end">
                <span>{amount}</span>
            </div>
        </div>
        '''
        row['amount'] = total

        row['actions'] = f'''
            <a  
                class="btn btn-sm btn-dark pt-1 pb-1" id="btn-bs-crud"
                data-form-url="{reverse_lazy('project:update-commitment', kwargs={'uid': obj.uid})}"
                data-async-update="true"
                data-element-id="#commitment-list"
                data-key="table"
                data-response-url="{reverse_lazy('portal:no_response')}"
            ><i class="fa fa-pencil"></i></a>
        <a class="btn btn-sm btn-danger pt-1 pb-1" 
            id="btn-bs-delete"
            data-form-url="{reverse_lazy('project:delete-commitment', kwargs={'pk': obj.pk})}"
            data-async-update="true"
            data-element-id="#commitment-list"
            data-key="table"
            data-response-url="{reverse_lazy('portal:no_response')}"
            data-is-delete="true"
        ><i class="fa fa-trash"></i></a>
        '''