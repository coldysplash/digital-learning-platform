from django.urls import path

from .views import CatalogView

app_name = "courses"

urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
]
