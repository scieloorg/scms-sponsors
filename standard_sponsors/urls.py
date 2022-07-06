from django.urls import path

from .views import import_file, validate

app_name = "standard_sponsors"
urlpatterns = [
    path("validate", view=validate, name="validate"),
    path("import", view=import_file, name="import_file"),
]
