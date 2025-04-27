from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path(
        "course/<int:pk>", views.CourseDetailView.as_view(), name="course_detail_view"
    ),
    path("enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path(
        "add_to_favorite/<int:course_id>/",
        views.add_to_favorites,
        name="add_to_favorites",
    ),
]
