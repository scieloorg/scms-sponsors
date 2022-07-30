import os

from django.db import models
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from core.models import CommonControlField
from .forms import ArticleSponsorsForm, ArticleSponsorsFileForm
from identified_sponsors.models import IdentifiedSponsors


class ArticleSponsors(CommonControlField):
    class Meta:
        verbose_name_plural = _('Article Sponsors')

    pid = models.CharField("PID", max_length=255, null=True, blank=True)
    sponsor_name = models.ForeignKey(IdentifiedSponsors, on_delete=models.SET_NULL, max_length=255, null=True, blank=True)
    project_id = models.CharField("Project ID", max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('pid'),
        FieldPanel('sponsor_name'),
        FieldPanel('project_id'),
    ]

    base_form_class = ArticleSponsorsForm


class ArticleSponsorsFile(CommonControlField):
    class Meta:
        verbose_name_plural = _('Article Sponsors Upload')

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
    base_form_class = ArticleSponsorsFileForm

