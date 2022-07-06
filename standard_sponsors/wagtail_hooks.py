from django.urls import include, path
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register, ModelAdminGroup)

from .button_helper import SponsorNamesStandardizedHelper
from .models import SponsorNamesStandardized, SponsorNamesStandardizedFile


class SponsorNamesStandardizedCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class SponsorNamesStandardizedFileCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class SponsorNamesStandardizedAdmin(ModelAdmin):
    model = SponsorNamesStandardized
    create_view_class = SponsorNamesStandardizedCreateView
    menu_label = 'Std Sponsors'
    menu_icon = 'folder'
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('sponsor_id', 'sponsor_name_std', 'sponsor_acron_std')
    # list_filter = ('sponsor_name_std',)
    search_fields = ('sponsor_name_std',)
    list_export = ('sponsor_id', 'sponsor_name_std', 'sponsor_acron_std')
    export_filename = 'standard_sponsor_names'


class SponsorNamesStandardizedFileAdmin(ModelAdmin):
    model = SponsorNamesStandardizedFile
    create_view_class = SponsorNamesStandardizedFileCreateView
    button_helper_class = SponsorNamesStandardizedHelper
    menu_label = 'Std Sponsors Upload'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('attachment', 'line_count', 'is_valid')
    list_filter = ('is_valid',)
    search_fields = ('attachment',)


class SponsorNamesStandardizedAdminGroup(ModelAdminGroup):
    menu_label = 'Std Sponsor Names'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (SponsorNamesStandardizedAdmin, SponsorNamesStandardizedFileAdmin,)


modeladmin_register(SponsorNamesStandardizedAdminGroup)


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('standard_sponsors/standardsponsorsfile/',
             include('standard_sponsors.urls', namespace='standard_sponsors')),

    ]
