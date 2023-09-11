from django.views.generic import DetailView
from django.http import Http404
from django.utils.translation import gettext as _
from fincapes.variables import aplikasi
from fincapes.mixins import ContextDataMixin, DropNewsletterSubscribesMixin
from contents.models import Content
"""

"""


class DetailArticleView(DropNewsletterSubscribesMixin, ContextDataMixin, DetailView):
    template_name = 'articles/index.html'
    model = Content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Article | ') + aplikasi.get('portal_app')
        context['app_name'] = aplikasi
        context['uri'] = 'article'
        return context