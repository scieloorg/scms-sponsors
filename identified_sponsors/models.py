import os

from django.db import models
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from core.models import CommonControlField
from .forms import IdentifiedSponsorsForm, IdentifiedSponsorsFileForm
from . import choices


class IdentifiedSponsors(CommonControlField):
    class Meta:
        verbose_name_plural = _('Identified Sponsors')

    declared_name = models.CharField(_("Declared Sponsor Name"), max_length=255, default=None, null=True, blank=False)
    official_name = models.CharField(_("Official Sponsor Name"), max_length=255, default=None, null=True, blank=False)
    official_acron = models.CharField(_("Official Sponsor Acronym"), max_length=255, default=None, null=True, blank=False)
    method = models.CharField(_("Identification Method"), max_length=255, choices=choices.IDENTIFICATION_METHOD, default=None, null=True, blank=False)
    score = models.DecimalField("Score", max_digits=4, decimal_places=3, null=True, blank=False)

    def __unicode__(self):
        return f"{self.official_name} ({self.official_acron})"

    def __str__(self):
        return f"{self.official_name} ({self.official_acron})"

    panels = [
        FieldPanel('declared_name'),
        FieldPanel('official_name'),
        FieldPanel('official_acron'),
        FieldPanel('method'),
        FieldPanel('score'),
    ]

    base_form_class = IdentifiedSponsorsForm


class IdentifiedSponsorsFile(CommonControlField):
    class Meta:
        verbose_name_plural = _('Identified Sponsors Upload')

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
    base_form_class = IdentifiedSponsorsFileForm
