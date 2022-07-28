from wagtail.admin.forms import WagtailAdminModelForm


class OfficialSponsorsForm(WagtailAdminModelForm):

    def save_all(self, user):
        official_sponsors = super().save(commit=False)

        if self.instance.pk is not None:
            official_sponsors.updated_by = user
        else:
            official_sponsors.creator = user

        self.save()

        return official_sponsors


class OfficialSponsorsFileForm(WagtailAdminModelForm):

    def save_all(self, user):
        official_sponsors_file = super().save(commit=False)

        if self.instance.pk is not None:
            official_sponsors_file.updated_by = user
        else:
            official_sponsors_file.creator = user

        self.save()

        return official_sponsors_file
