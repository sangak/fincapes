from django import forms
from django.utils.translation import gettext as _
from .models import Awp, SubActivity
from django.urls import reverse_lazy
from bootstrap_modal_forms.forms import (
    BSModalModelForm
)
from projects.models import Output
from crispy_forms.helper import FormHelper
from django.forms import modelformset_factory
from crispy_forms.layout import Layout, Column, Row, Div, Fieldset, Field
from crispy_forms.bootstrap import StrictButton
from django_select2.forms import ModelSelect2Widget
from fincapes import variables


class AwpBSModelForm(BSModalModelForm):
    output = forms.ModelChoiceField(
        empty_label=variables.label_settings.get('please_select'),
        queryset=Output.objects.all(),
        label='Output',
        required=False,
        widget=ModelSelect2Widget(
            model=Output,
            search_fields=['code__icontains', 'description__icontains'],
            attrs=variables.SELECT_WIDGET_MODEL_WITH_SEARCH_ATTRS,
        )
    )

    sorted_num = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'id': 'sorted_num'
        })
    )
    title = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Enter the activity'),
            'class': 'no-resize',
            'rows': 3,
            'id': 'activity'
        })
    )

    class Meta:
        model = Awp
        fields = ['output', 'sorted_num', 'title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('output'),
                    css_class='form-group'
                ),
                Div(
                    Fieldset(
                        'Activity',
                        Row(
                            Column('sorted_num', css_class='col-lg-2'),
                            Column('title', css_class='col-lg-10')
                        ),
                    ),
                    css_class='form-group'
                ),
                css_class='modal-body'
            )
        )