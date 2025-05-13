from django.urls import path

from . import views

app_name = "construct"

urlpatterns = [
    path("course/<int:pk>/", views.ConstructorCourseView.as_view(), name="main"),
    path(
        "course/<int:course_id>/module/create/",
        views.ModuleCreateView.as_view(),
        name="module_create",
    ),
    path("module/<int:pk>/", views.ModuleDetailView.as_view(), name="module"),
    path("module/<int:pk>/edit/", views.ModuleUpdateView.as_view(), name="module_edit"),
    path(
        "module/<int:pk>/delete/",
        views.module_delete,
        name="module_delete",
    ),
    path(
        "module/<int:module_id>/lesson/create/",
        views.LessonCreateView.as_view(),
        name="lesson_create",
    ),
    path("lesson/<int:pk>/", views.LessonDetailView.as_view(), name="lesson"),
    path("lesson/<int:pk>/edit/", views.LessonUpdateView.as_view(), name="lesson_edit"),
    path(
        "lesson/<int:pk>/delete/",
        views.lesson_delete,
        name="lesson_delete",
    ),
]
