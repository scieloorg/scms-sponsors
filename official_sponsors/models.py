import os

from django.db import models
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from core.models import CommonControlField
from .forms import OfficialSponsorsForm, OfficialSponsorsFileForm


class OfficialSponsorNames(CommonControlField):
    class Meta:
        verbose_name_plural = _('Official Sponsor Name')

    official_sponsor_name = models.CharField("Official Name", max_length=255, null=False, blank=False)
    official_sponsor_acron = models.CharField("Official Acronym", max_length=255, null=False, blank=False)

    panels = [
        FieldPanel('official_sponsor_name'),
        FieldPanel('official_sponsor_acron'),
    ]
    base_form_class = OfficialSponsorsForm


class OfficialSponsorNamesFile(CommonControlField):
    class Meta:
        verbose_name_plural = _('Official Sponsor Name Upload')

    attachment = models.ForeignKey(
        'wagtaildocs.Document',
        null=True, blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    is_valid = models.BooleanField(_("É valido?"), default=False, blank=True, null=True)
    line_count = models.IntegerField(_("Quantidade de linhas"), default=0, blank=True, null=True)

    def filename(self):
        return os.path.basename(self.attachment.name)

    panels = [
        DocumentChooserPanel('attachment')
    ]
    base_form_class = OfficialSponsorsFileForm
