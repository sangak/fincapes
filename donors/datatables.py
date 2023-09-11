from django.utils.translation import gettext as _
from .models import Donor
from django.urls import reverse_lazy
from fincapes.helpers import DatatableView


class DonorAjaxListView(DatatableView):
    model = Donor
    title = _('List of Donors')
    initial_order = []
    search_values_separator = '+'
    show_date_filters = False
    show_column_filters = False

    column_defs = [
        {'name': 'title', 'title': _('Donor'), 'searchable': True, 'visible': True, "width": "45%", },
        {'name': 'acronym', 'title': _('Acronym'), 'searchable': True, 'visible': True, },
        {'name': 'status', 'title': 'Status', 'searchable': True, 'visible': True, },
        {'name': 'actions', 'title': "", "orderable": False, "width": "10%", 'searchable': False, }
    ]

    def get_initial_queryset(self, request=None):
        return Donor.objects.all()

    def customize_row(self, row, obj):
        colors = ['warning', 'success', 'danger']
        status = f'''
        <span class="badge rounded-pill bg-{colors[obj.status]}">{obj.get_status_display()}</span>
        '''
        row['status'] = status

        row['actions'] = f'''
            <a  
                class="btn btn-sm btn-dark pt-1 pb-1" id="btn-bs-crud"
                data-form-url="{reverse_lazy('donor:update', kwargs={'uid': obj.uid})}"
                data-async-update="true"
                data-element-id="#donor-list"
                data-key="table"
                data-response-url="{reverse_lazy('portal:no_response')}"
            ><i class="fa fa-pencil"></i></a>
        <a class="btn btn-sm btn-danger pt-1 pb-1" 
            id="btn-bs-delete"
            data-form-url="{reverse_lazy('donor:delete', kwargs={'pk': obj.pk})}"
            data-async-update="true"
            data-element-id="#donor-list"
            data-key="table"
            data-response-url="{reverse_lazy('portal:no_response')}"
            data-is-delete="false"
        ><i class="fa fa-trash"></i></a>
        '''
        return