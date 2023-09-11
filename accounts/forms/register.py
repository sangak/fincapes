from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row, Column, Field, Div
from fincapes.helpers import Submit
from fincapes import variables

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First name'),
                'autofocus': 'autofocus',
                'autocomplete': 'off',
                'spellcheck': 'false'
            }
        ),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last name'),
                'autocomplete': 'off',
                'spellcheck': 'false'
            }
        ),
        required=False
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'autocomplete': 'off'
            }
        ),
        required=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
            }
        ),
        required=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Re-type your password')
            }
        ),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]

    def __init__(self, *args, **kwargs):
        meta = self.Meta.model._meta
        fname = meta.get_field('first_name').max_length
        lname = meta.get_field('last_name').max_length
        email_length = meta.get_field('email').max_length
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['maxlength'] = fname
        self.fields['last_name'].widget.attrs['maxlength'] = lname
        self.fields['email'].widget.attrs['maxlength'] = email_length
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-lg-6'),
                Column('last_name', css_class='col-lg-6'),
                css_class='g-2'
            ),
            Row(
                Column('email')
            ),
            Row(Column('password1')),
            Row(Column('password2')),
            Row(
                Column(
                    Submit('submit', _('Register'), css_class='btn-primary', css_id='btn-register')
                )
            )
        )