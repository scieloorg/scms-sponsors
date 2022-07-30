from wagtail.admin.forms import WagtailAdminModelForm


class IdentifiedSponsorsForm(WagtailAdminModelForm):

    def save_all(self, user):
        identified_sponsors = super().save(commit=False)

        if self.instance.pk is not None:
            identified_sponsors.updated_by = user
        else:
            identified_sponsors.creator = user

        self.save()

        return identified_sponsors


class IdentifiedSponsorsFileForm(WagtailAdminModelForm):

    def save_all(self, user):
        identified_sponsors_file = super().save(commit=False)

        if self.instance.pk is not None:
            identified_sponsors_file.updated_by = user
        else:
            identified_sponsors_file.creator = user

        self.save()

        return identified_sponsors_file

