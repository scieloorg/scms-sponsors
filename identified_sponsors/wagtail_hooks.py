from django.urls import include, path
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register, ModelAdminGroup)

from .button_helper import IdentifiedSponsorsHelper
from .models import IdentifiedSponsors, IdentifiedSponsorsFile


class IdentifiedSponsorsCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class IdentifiedSponsorsFileCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class IdentifiedSponsorsAdmin(ModelAdmin):
    model = IdentifiedSponsors
    create_view_class = IdentifiedSponsorsCreateView
    menu_label = 'Identified Sponsors'
    menu_icon = 'folder'
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('sponsor_name', 'std_id_jac', 'score_jac', 'std_id_sem', 'score_sem')
    # list_filter = ('sponsor_name',)
    search_fields = ('sponsor_name',)
    list_export = ('sponsor_name', 'std_id_jac', 'score_jac', 'std_id_sem', 'score_sem')
    export_filename = 'identified_sponsors'


class IdentifiedSponsorsFileAdmin(ModelAdmin):
    model = IdentifiedSponsorsFile
    create_view_class = IdentifiedSponsorsFileCreateView
    button_helper_class = IdentifiedSponsorsHelper
    menu_label = 'Identified Sponsors Upload'  # ditch this to use verbose_name_plural from model
    menu_icon = 'folder'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('attachment', 'line_count', 'is_valid')
    list_filter = ('is_valid',)
    search_fields = ('attachment',)


class IdentifiedSponsorsAdminGroup(ModelAdminGroup):
    menu_label = 'Identified Sponsors'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (IdentifiedSponsorsAdmin, IdentifiedSponsorsFileAdmin,)


modeladmin_register(IdentifiedSponsorsAdminGroup)


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('identified_sponsors/identifiedsponsorsfile/',
             include('identified_sponsors.urls', namespace='identified_sponsors')),

    ]
