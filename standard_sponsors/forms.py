from wagtail.admin.forms import WagtailAdminModelForm


class StandardSponsorsForm(WagtailAdminModelForm):

    def save_all(self, user):
        standard_sponsors = super().save(commit=False)

        if self.instance.pk is not None:
            standard_sponsors.updated_by = user
        else:
            standard_sponsors.creator = user

        self.save()

        return standard_sponsors


class StandardSponsorsFileForm(WagtailAdminModelForm):

    def save_all(self, user):
        standard_sponsors_file = super().save(commit=False)

        if self.instance.pk is not None:
            standard_sponsors_file.updated_by = user
        else:
            standard_sponsors_file.creator = user

        self.save()

        return standard_sponsors_file

