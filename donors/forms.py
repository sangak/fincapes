from django import forms
from django.utils.translation import gettext as _
from .models import Donor
from django.utils.safestring import mark_safe
from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Div, HTML
from crispy_forms.bootstrap import StrictButton
from django_select2.forms import Select2Widget
from fincapes.variables import (
    DONOR_STATUS_CHOICES, label_settings
)


class DonorBSModelForm(BSModalModelForm):
    title = forms.CharField(
        label=mark_safe(_('Donor name') + label_settings.get('required')),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Type the donor name')
            }
        )
    )

    acronym = forms.CharField(
        label=mark_safe(_('Acronym') + label_settings.get('required')),
        required=False,
        widget=forms.TextInput()
    )

    status = forms.ChoiceField(
        label='Status',
        required=False,
        choices=DONOR_STATUS_CHOICES,
        initial=0,
        widget=Select2Widget(
            attrs={
                'data-placeholder': _('Please select ...'),
                'data-minimum-results-for-search': 'Infinity',
                'data-allow-clear': False
            }
        )
    )

    class Meta:
        model = Donor
        fields = ['title', 'acronym', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('title')
                ),
                Row(
                    Column('acronym', css_class='col-lg-6'),
                    Column('status', css_class='col-lg-6')
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

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError(label_settings.get('no_blank') % _('Donor name'))
        return title

    def clean_acronym(self):
        acronym = self.cleaned_data.get('acronym')
        if not acronym:
            raise forms.ValidationError(label_settings.get('no_blank') % _('Acronym'))
        return acronym


class DonorBSDeleteForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['title', 'acronym', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Row(
                    Column(
                        HTML(f'''
                        <p>{_('Are you sure to delete this?')}</p>
                        ''')
                    )
                ),
                css_class='modal-body'
            ),
            Div(
                Row(
                    Div(
                        StrictButton(
                            _('Delete'),
                            type='submit',
                            css_class='btn-primary',
                            css_id='btn-bs-submit'
                        )
                    )
                ),
                css_class='modal-footer border-top-0'
            )
        )