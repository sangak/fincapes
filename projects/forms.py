from django import forms
from django.utils.translation import gettext as _
from .models import Project
from django.utils.safestring import mark_safe
from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Div, HTML, Fieldset
from crispy_forms.bootstrap import StrictButton, FieldWithButtons
from django_select2.forms import Select2Widget, ModelSelect2Widget
from fincapes.helpers import check_date_valid
from fincapes.variables import label_settings, CURRENCY_CHOICES, SELECT_WIDGET_ATTRS
from donors.models import Donor
from .models import Commitment, UltimateOutcome, IntermediateOutcome


class ProjectModelForm(forms.ModelForm):
    title = forms.CharField(
        required=False,
        label=mark_safe(_('Project name') + label_settings.get('required')),
        widget=forms.TextInput(attrs={
            'id': 'project-name'
        })
    )
    acronym = forms.CharField(
        label=_('Acronym'),
        required=False,
        widget=forms.TextInput()
    )
    project_start = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Start date'),
            'class': 'date-period',
            'id': 'start-date'
        })
    )
    project_end = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('End date'),
            'class': 'date-period',
            'id': 'end-date'
        })
    )
    brief_description = forms.CharField(
        label=_('Brief Description'),
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': _('Enter a brief description related to the project'),
            'class': "no-resize"
        })
    )

    class Meta:
        model = Project
        fields = ['title', 'acronym', 'brief_description',
                  'project_start', 'project_end'
                  ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs['initial'] = {
                'project_start': instance.get_local_project_start('id'),
                'project_end': instance.get_local_project_end('id')
            }
        # if instance:
        #     # self.fields['title'].widget.attrs['readonly'] = True

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'frm-project-update'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-lg-6'),
                Column('acronym', css_class='col-lg-3'),
                css_class='mb-3 form-group'
            ),
            Row(
                Fieldset(
                    _('Project period'),
                    Row(
                        Column('project_start', css_class='col-lg-2'),
                        Column('project_end', css_class='col-lg-2')
                    ),
                    css_class='date-picker', data_inputs='.date-period'
                ),
                css_class='mb-3 form-group'
            ),
            Row(
                Column('brief_description', css_class='col-lg-7')
            )
        )

    def clean_project_start(self):
        start = self.cleaned_data.get('project_start')
        correct, new_date = check_date_valid(start)
        if correct:
            return new_date
        return None

    def clean_project_end(self):
        end = self.cleaned_data.get('project_end')
        correct, new_date = check_date_valid(end)
        if correct:
            return new_date
        return None

    # def save(self, commit=True):
    #     project = super().save(commit=False)
    #     if commit:
    #         st_true, new_start = check_date_valid(self.cleaned_data.get('pro_start'))
    #         et_true, new_end = check_date_valid(self.cleaned_data.get('pro_end'))
    #         project.project_start = new_start
    #         project.project_end = new_end
    #         project.save()
    #     return project


class CommitmentBSModelForm(BSModalModelForm):
    donor = forms.ModelChoiceField(
        label='Donor',
        required=False,
        queryset=Donor.objects.active(),
        widget=Select2Widget(attrs=SELECT_WIDGET_ATTRS)
    )
    currency = forms.ChoiceField(
        label=_('Currency'),
        required=False,
        choices=CURRENCY_CHOICES,
        widget=Select2Widget(attrs=SELECT_WIDGET_ATTRS)
    )
    amount = forms.CharField(
        label=_('Amount'),
        required=False,
        widget=forms.TextInput()
    )

    class Meta:
        model = Commitment
        fields = ['donor', 'currency', 'amount', 'project']

    def __init__(self, project, *args, **kwargs):
        self.parent_project = project
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('donor')
                ),
                Row(
                    Column('currency', css_class='col-lg-3'),
                    Column('amount', css_class='col-lg-9')
                ),
                css_class='modal-body'
            ),
            Div(
                Row(
                    Column(
                        StrictButton(
                            _('Save'),
                            type='submit',
                            css_class='btn-primary',
                            css_id='btn-bs-submit'
                        )
                    )
                ),
                css_class='modal-footer'
            )
        )

    def save(self, commit=True):
        commitment = super().save(commit=False)
        if commit:
            commitment.project = self.parent_project
            commitment.save()
        return commitment


class UltimateBSOutcomeForm(BSModalModelForm):
    project = forms.ModelChoiceField(
        label=_('Project name'),
        required=False,
        queryset=Project.objects.all(),
        widget=Select2Widget(attrs=SELECT_WIDGET_ATTRS)
    )
    code = forms.CharField(
        label=_('Code'),
        required=False,
        initial=1000,
        widget=forms.TextInput(attrs={
            'readonly': True
        })
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
            'class': 'no-resize',
            'rows': 4
        })
    )

    class Meta:
        model = UltimateOutcome
        fields = ['project', 'code', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('project', css_class='col-lg-8'),
                    Column('code', css_class='col-lg-4')
                ),
                Row(Column('description')),
                css_class='modal-body'
            ),
            Div(
                Column(
                    StrictButton(
                        _('Save'), type="submit", css_class='btn btn-inverse-blue'
                    )
                ),
                css_class='modal-footer border-top-0 text-end'
            )
        )


class IntermediateBSOutcomeForm(BSModalModelForm):
    code = forms.CharField(
        label=_('Code'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-25'
        })
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Description'),
            'class': 'no-resize',
            'rows': 5
        })
    )

    class Meta:
        model = IntermediateOutcome
        fields = ['code', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('code'),
                    css_class='form-group'
                ),
                Div(
                    Div('description', css_class='col-lg-12'),
                    css_class='form-group'
                ),
                css_class='modal-body mb-0 pb-0'
            ),
            Div(
                StrictButton(
                    _('Save'), type="submit", css_class='btn btn-inverse-blue'
                ),
                css_class='modal-footer text-end border-top-0'
            )
        )