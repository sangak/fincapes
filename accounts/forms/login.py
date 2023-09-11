from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, HTML, Column
from crispy_forms.bootstrap import FieldWithButtons
from fincapes.helpers import email_validator, Submit

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
                'spellcheck': 'false',
                'id': 'email'
            }
        ),
        required=False
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'id': 'password'
            }
        ),
        required=False,
        help_text=mark_safe(f'''
            <div class="d-flex mt-2 align-self-end justify-content-end">
                <a href="#">{_('Forgot password?')}</a>
            </div>
        ''')
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.form_id = 'login-form'
        self.helper.layout = Layout(
            Row(
                Column('email')
            ),
            Row(
                Column(
                    'password',
                    css_class='text-end'
                )
            ),
            Div(
                Submit('submit', _('Login'), css_class='btn-primary', css_id='btn-login'),
                css_class='mt-4'
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_('Email address should not be blank'))
        if not email_validator(email):
            raise forms.ValidationError(
                _('Your email is not valid! Please enter a valid email address.')
            )
        return email

    def clean_password(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        if not password:
            raise forms.ValidationError(_('Password should not be blank!'))

        qs = User.objects.filter(email=email)
        if not qs.exists():
            err = forms.ValidationError(_('The email was not found'))
            self.add_error('email', err)

        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError(_('Incorrect password! Please re-type your password'))
        login(request, user)
        self.user = user
        return data