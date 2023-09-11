from django import forms
from django.utils.translation import gettext as _
from django.urls import reverse
from crispy_forms.layout import Layout, Column, Row, Field
from crispy_forms.helper import FormHelper
from django_select2.forms import Select2Widget
from fincapes.helpers import email_validator, Submit
from fincapes.variables import languages
from subscribers.models import Subscriber
# from subscribes.models import NewsletterSubscriber


class ChangeLanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=languages,
        widget=Select2Widget(attrs={
            'data-minimum-results-for-search': 'Infinity',
            'data-allow-clear': False,
            'id': 'language'
        }),
        required=False
    )

    def __init__(self, bahasa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['language'].initial = bahasa
        # self.helper.field_template = 'bootstrap5/field2.html'
        self.helper.form_group_wrapper_class = 'mb-0'
        self.helper.form_action = reverse('set_language')


class NewspaperSubscribeForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Full name')
        }),
        required=False
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'}
        ),
        required=False
    )

    class Meta:
        model = Subscriber
        fields = ['full_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'full_name',
                    css_class='col-md-5 col-sm-6'
                ),
                Column(
                    'email',
                    css_class='col-md-5 col-sm-6'
                ),
                Column(
                    Submit('submit', _('Subscribe Now'), css_class='btn-outline-warning'),
                    css_class='col-md-2 col-sm-12 mt-md-0 mt-sm-4'
                )
            )
        )

    def save(self, commit=True):
        subscriber = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name')
        email = self.cleaned_data.get('email')
        if commit:
            subscriber.full_name = full_name
            subscriber.email = email
            subscriber.save()
        return subscriber