import os

from django.db import models
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from core.models import CommonControlField
from .forms import StandardSponsorsForm, StandardSponsorsFileForm


class SponsorNamesStandardized(CommonControlField):
    class Meta:
        verbose_name_plural = _('Sponsor Name Standardized')

    sponsor_id = models.IntegerField("ID", null=True, blank=False)
    sponsor_name_std = models.CharField("Standard Name", max_length=255, null=True, blank=True)
    sponsor_acron_std = models.CharField("Standard Acronym", max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('sponsor_id'),
        FieldPanel('sponsor_name_std'),
        FieldPanel('sponsor_acron_std'),
    ]
    base_form_class = StandardSponsorsForm


class SponsorNamesStandardizedFile(CommonControlField):
    class Meta:
        verbose_name_plural = _('Sponsor Name Standardized Upload')

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
    base_form_class = StandardSponsorsFileForm

