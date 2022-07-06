import os

from django.db import models
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from core.models import CommonControlField
from .forms import IdentifiedSponsorsForm, IdentifiedSponsorsFileForm


class IdentifiedSponsors(CommonControlField):
    class Meta:
        verbose_name_plural = _('Identified Sponsors')

    sponsor_name = models.CharField("Sponsor Name", max_length=255, null=True, blank=True)
    std_id_jac = models.IntegerField("ID (Jaccard)", null=True, blank=True)
    score_jac = models.DecimalField("Score (Jaccard)", max_digits=4, decimal_places=3, null=True, blank=True)
    std_id_sem = models.IntegerField("ID (Semantic)", null=True, blank=True)
    score_sem = models.DecimalField("Score (Semantic)", max_digits=4, decimal_places=3, null=True, blank=True)

    panels = [
        FieldPanel('sponsor_name'),
        FieldPanel('std_id_jac'),
        FieldPanel('score_jac'),
        FieldPanel('std_id_sem'),
        FieldPanel('score_sem'),
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
