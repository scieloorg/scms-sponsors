from wagtail.admin.forms import WagtailAdminModelForm


class ArticleSponsorsForm(WagtailAdminModelForm):

    def save_all(self, user):
        article_sponsors = super().save(commit=False)

        if self.instance.pk is not None:
            article_sponsors.updated_by = user
        else:
            article_sponsors.creator = user

        self.save()

        return article_sponsors


class ArticleSponsorsFileForm(WagtailAdminModelForm):

    def save_all(self, user):
        article_sponsors_file = super().save(commit=False)

        if self.instance.pk is not None:
            article_sponsors_file.updated_by = user
        else:
            article_sponsors_file.creator = user

        self.save()

        return article_sponsors_file

