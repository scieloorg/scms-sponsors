from django.urls import include, path
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register, ModelAdminGroup)

from .button_helper import OfficialSponsorNamesHelper
from .models import OfficialSponsorNames, OfficialSponsorNamesFile


class OfficialSponsorNamesCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class OfficialSponsorNamesFileCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class OfficialSponsorNamesAdmin(ModelAdmin):
    model = OfficialSponsorNames
    create_view_class = OfficialSponsorNamesCreateView
    menu_label = _('Official Sponsors')
    menu_icon = 'folder'
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('official_sponsor_name', 'official_sponsor_acron')
    search_fields = ('official_sponsor_name',)
    list_export = ('official_sponsor_name', 'official_sponsor_acron')
    export_filename = 'official_sponsor_names'


class OfficialSponsorNamesFileAdmin(ModelAdmin):
    model = OfficialSponsorNamesFile
    create_view_class = OfficialSponsorNamesFileCreateView
    button_helper_class = OfficialSponsorNamesHelper
    menu_label = 'Official Sponsors Upload'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('attachment', 'line_count', 'is_valid')
    list_filter = ('is_valid',)
    search_fields = ('attachment',)


class OfficialSponsorNamesAdminGroup(ModelAdminGroup):
    menu_label = 'Official Sponsor Names'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (OfficialSponsorNamesAdmin, OfficialSponsorNamesFileAdmin,)


modeladmin_register(OfficialSponsorNamesAdminGroup)


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('official_sponsors/officialsponsorsfile/',
             include('official_sponsors.urls', namespace='official_sponsors')),

    ]
