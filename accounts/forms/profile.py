from django import forms
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from image_cropping import ImageCropWidget
from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Row, Column, Fieldset
from django_select2.forms import Select2Widget, Select2MultipleWidget
from fincapes import variables
from fincapes.helpers import check_date_valid, Submit
from ..models import Profile

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        label=_('Full name'),
        widget=forms.TextInput(
            attrs={
                'id': 'full-name',
                'spellcheck': 'false',
                'autocomplete': 'off',
                'disabled': 'disabled'
            }
        ),
        required=False
    )
    area_code = forms.CharField(
        label='',
        required=False,
        max_length=3,
        widget=forms.TextInput(
            attrs={
                'placeholder': '62'
            }
        )
    )
    phone_no = forms.CharField(
        label='',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'id': 'no-tel',
                'placeholder': '8xx-xxxx-xxxx'
            }
        ),
        required=False
    )
    gender = forms.ChoiceField(
        label=_('Gender'),
        choices=variables.GENDER_CHOICES,
        required=False,
        widget=Select2Widget(
            attrs={
                'data-placeholder': _('Please select ...'),
                'data-minimum-results-for-search': 'Infinity',
                'data-allow-clear': False,
                'id': 'gender'
            }
        )
    )
    language = forms.ChoiceField(
        label=_('Prefer language'),
        choices=variables.languages,
        widget=Select2Widget(
            attrs={
                'data-placeholder': _('Please select ...'),
                'data-minimum-results-for-search': 'Infinity',
                'data-allow-clear': 'false'
            }
        ),
        required=False
    )
    timezone = forms.ChoiceField(
        label=_('Timezone'),
        required=False,
        choices=variables.TIMEZONES,
        widget=Select2Widget(
            attrs={
                'data-placeholder': _('Please select ...'),
                'data-minimum-results-for-search': 'Infinity',
                'data-allow-clear': 'false'
            }
        )
    )

    class Meta:
        model = Profile
        fields = [
            'no_tel', 'gender', 'language', 'timezone'
        ]

    def __init__(self, *args, **kwargs):
        meta = self.Meta.model._meta
        tel_length = meta.get_field('no_tel').max_length
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['phone_no'].max_length = tel_length
            code, phone = instance.split_tel
            self.fields['area_code'].initial = code
            self.fields['phone_no'].initial = phone
        self.helper = FormHelper()
        self.helper.field_class = 'mb-4'
        self.helper.layout = Layout(
            Row(
                Column(
                    Fieldset(
                        _('Phone No. / Whatsapp') + '<span class="text-danger">*</span>',
                        Row(
                            Column('area_code', css_class='col-lg-3 col-sm-4'),
                            Column('phone_no', css_class='col-lg-9 col-sm-8'),
                            css_class='g-1 mt-0'
                        )
                    ),
                    css_class='col-lg-8 col-sm-12'
                ),
                Column('gender', css_class='col-lg-4 col-sm-12')
            ),
            Row(
                Column('language', css_class='col-lg-6'),
                Column('timezone')
            ),
            Row(
                Column(
                    HTML('<hr>')
                )
            ),
            Row(
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary float-end')
                )
            )
        )

    def clean_area_code(self):
        area_code = self.cleaned_data.get('area_code')
        if not area_code:
            raise forms.ValidationError(_('Enter the code'))
        return area_code

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if not phone_no:
            raise forms.ValidationError(_('Phone number should not be blank'))
        return phone_no

    def save(self, commit=True):
        profil = super(UserProfileForm, self).save(commit=False)
        code = self.cleaned_data.get('area_code')
        phone = self.cleaned_data.get('phone_no')
        if commit:
            profil.no_tel = f"{code}-{phone}"
            profil.save()
            profil.profile_filled()
        return profil
    # def clean_area_code(self):
    #     area_code = self.cleaned_data.get('area_code')
    #     if not area_code:
    #         err = forms.ValidationError(_('Enter a code'))
    #         raise err
    #     return area_code


class BSUploadAvatarForm(BSModalModelForm):
    class Meta:
        widgets = {
            'photo': ImageCropWidget
        }