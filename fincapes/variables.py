from django.utils.translation import gettext_lazy as _

aplikasi = {
    'project': 'FINCAPES',
    'portal_app': _('FINCAPES Project'),
    'portal_name': 'FINCAPES<span>Portal</span>',
    'domain': 'fincapes.com',
    'required': '<span class="text-danger">*</span>',
    'version': 'alpha 1.0'
}

CURRENCY_CHOICES = (
    (1, 'CAD'),
    (2, 'IDR'),
    (3, 'USD')
)

STATUS_CHOICES = (
    (1, 'draft'),
    (2, 'active')
)

DONOR_STATUS_CHOICES = (
    (0, 'Draft'),
    (1, 'Active'),
    (2, 'Inactive')
)

DONOR_TYPE_CHOICES = (
    (1, _('Government')),
    (2, _('Private/Business'))
)

languages = (
    ('id', _('Indonesia')),
    ('en', _('English'))
)

menu_setting = {
    'change_password': _('Change Password'),
    'sign_in': _('Sign in'),
    'sign_out': _('Sign out'),
    'sign_up': _('Register'),
    'resend_activation': _('Resend activation'),
    'activated': _('Activated'),
    'add_new': _('Add New'),
    'cancel': _('Cancel'),
    'dashboard': _('Dashboard'),
    'delete': _('Delete'),
    'edit': _('Edit'),
    'finish': _('Finish'),
    'next': _('Next'),
    'previous': _('Previous'),
    'forgot_password': _('Forgot password'),
    'reset_password': _('Reset Password'),
    'user_profile': _('User Profile'),
    'save': _('Save'),
    'share': _('Share'),
    'search': _('Search'),
    'submit': _('Submit'),
    'update': _('Update')
}

USER_TYPE_CHOICES = (
    (1, 'FINCAPES'),
    (2, 'uWaterloo'),
    (3, _('Partners')),
    (4, _('Beneficiaries'))
)
USER_CATEGORY_CHOICES = (
    (1, _('Director')),
    (2, _('Program Officer')),
    (3, _('Administrative')),
    (4, _('Finance'))
)

GENDER_CHOICES = (
    (1, _('Female')),
    (2, _('Male'))
)

TIMEZONES = (
    ('Canada/Atlantic', 'Canada/Atlantic'),
    ('Canada/Central', 'Canada/Central'),
    ('Canada/Eastern', 'Canada/Eastern'),
    ('Canada/Mountain', 'Canada/Mountain'),
    ('Canada/Newfoundland', 'Canada/Newfoundland'),
    ('Canada/Pacific', 'Canada/Pacific'),
    ('Canada/Saskatchewan', 'Canada/Saskatchewan'),
    ('Canada/Yukon', 'Canada/Yukon'),
    ('Asia/Jakarta', 'Jakarta/WIB'),
    ('Asia/Makassar', 'Makassar/WITA'),
    ('Asia/Jayapura', 'Jayapura/WIT'),
)

label_settings = {
    'no_data_available': _('No data available'),
    'until': _('until'),
    'page404': _('Sorry, this page not available'),
    'please_select': _('---- Please select ----'),
    'no_blank': _('%s should not be blank'),
    'required': '<span class="text-danger">*</span>'
}

SELECT_WIDGET_ATTRS = {
    'data-placeholder': label_settings.get('please_select'),
    'data-minimum-results-for-search': 'Infinity',
    'data-allow-clear': False
}
SELECT_WIDGET_MODEL_NO_SEARCH_ATTRS = {
    'data-minimum-results-for-search': 'Infinity',
    "data-minimum-input-length": 0,
    "data-allow-clear": False
}
SELECT_WIDGET_MODEL_WITH_SEARCH_ATTRS = {
    "data-minimum-input-length": 0,
    "data-allow-clear": False
}

ADDRESS_CHOICES = (
    (1, _('Office')),
    (2, _('Home')),
)

page_title = {
    'project_info': _('Project Information')
}