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
        {'name': 'title', 'title': _('Donor'), 'orderable': True, 'searchable': True, 'visible': True, "width": "45%", },
        {'name': 'acronym', 'title': _('Acronym'), 'orderable': True, 'searchable': True, 'visible': True, },
        {'name': 'status', 'title': 'Status', 'orderable': True, 'searchable': True, 'visible': True, },
        {'name': 'actions', 'title': "", "orderable": False, "width": "5%", 'searchable': False, }
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
            <div class="dropdown mb-0">
                <button class="btn p-0 btn-default" type="button" id="dropdownMenuAction" data-bs-toggle="dropdown" 
                aria-haspopup="true" aria-expanded="false">
                    <i class="icon-lg text-muted" data-feather="more-horizontal"></i>
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuAction">
                    <a 
                        class="dropdown-item d-flex align-items-center p-2" id="btn-bs-crud"
                        data-form-url="{reverse_lazy('donor:update', kwargs={'uid': obj.uid})}"
                        data-async-update="true"
                        data-element-id="#donor-list"
                        data-key="table"
                        data-response-url="{reverse_lazy('portal:no_response')}">
                        <i data-feather="edit-2" class="icon-sm me-2"></i>
                        <span class="">Edit</span>
                    </a>
                    <a class="dropdown-item d-flex align-items-center p-2" 
                        id="btn-bs-delete"
                        data-form-url="{reverse_lazy('donor:delete', kwargs={'pk': obj.pk})}"
                        data-is-delete="true">
                        <i class="icon-sm me-2 text-danger" data-feather="trash"></i>
                        <span class="text-danger">Delete</span>
                    </a>
                </div>
            </div>
        '''