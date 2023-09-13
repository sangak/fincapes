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
            <div class="dropdown mb-0">
                <button class="btn p-0 btn-default" type="button" id="dropdownMenuAction" data-bs-toggle="dropdown" 
                aria-haspopup="true" aria-expanded="false">
                    <i class="icon-lg text-muted" data-feather="more-horizontal"></i>
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuAction">
                    <a 
                        class="dropdown-item d-flex align-items-center p-2" id="btn-bs-crud"
                        data-form-url="{reverse_lazy('project:update-commitment', kwargs={'uid': obj.uid})}"
                        data-async-update="true"
                        data-element-id="#donor-list"
                        data-key="table"
                        data-response-url="{reverse_lazy('portal:no_response')}">
                        <i data-feather="edit-2" class="icon-sm me-2"></i>
                        <span class="">Edit</span>
                    </a>
                    <a class="dropdown-item d-flex align-items-center p-2" 
                        id="btn-bs-delete"
                        data-form-url="{reverse_lazy('project:delete-commitment', kwargs={'pk': obj.pk})}"
                        data-is-delete="true">
                        <i class="icon-sm me-2 text-danger" data-feather="trash"></i>
                        <span class="text-danger">Delete</span>
                    </a>
                </div>
            </div>
        '''