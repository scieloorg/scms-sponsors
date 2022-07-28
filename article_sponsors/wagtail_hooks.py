from django.urls import include, path
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register, ModelAdminGroup)

from .button_helper import ArticleSponsorsHelper
from .models import ArticleSponsors, ArticleSponsorsFile


class ArticleSponsorsCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class ArticleSponsorsFileCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class ArticleSponsorsAdmin(ModelAdmin):
    model = ArticleSponsors
    create_view_class = ArticleSponsorsCreateView
    menu_label = 'Article Sponsors'
    menu_icon = 'folder'
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('pid', 'sponsor_name', 'project_id')
    # list_filter = ('sponsor_name',)
    search_fields = ('sponsor_name',)
    list_export = ('pid', 'sponsor_name', 'project_id')
    export_filename = 'article_sponsors'


class ArticleSponsorsFileAdmin(ModelAdmin):
    model = ArticleSponsorsFile
    create_view_class = ArticleSponsorsFileCreateView
    button_helper_class = ArticleSponsorsHelper
    menu_label = 'Article Sponsors Upload'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('attachment', 'line_count', 'is_valid')
    list_filter = ('is_valid',)
    search_fields = ('attachment',)


class ArticleSponsorsAdminGroup(ModelAdminGroup):
    menu_label = 'Article Sponsors'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ArticleSponsorsAdmin, ArticleSponsorsFileAdmin,)


modeladmin_register(ArticleSponsorsAdminGroup)


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('article_sponsors/articlesponsorsfile/',
             include('article_sponsors.urls', namespace='article_sponsors')),

    ]
