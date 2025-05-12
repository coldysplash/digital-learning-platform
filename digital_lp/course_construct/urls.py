from django.urls import path

from . import views

app_name = "construct"

urlpatterns = [
    path("course/<int:course_id>/", views.ModuleListView.as_view(), name="main"),
    path(
        "course/<int:course_id>/module/create/",
        views.ModuleCreateView.as_view(),
        name="module_create",
    ),
    path("module/<int:pk>/", views.ModuleDetailView.as_view(), name="module"),
    path("module/<int:pk>/edit/", views.ModuleUpdateView.as_view(), name="module_edit"),
    path(
        "module/<int:module_id>/delete/",
        views.module_delete,
        name="module_delete",
    ),
]
