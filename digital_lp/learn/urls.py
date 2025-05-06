from django.urls import path

from . import views

app_name = "learn"

urlpatterns = [
    path("enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path(
        "add_to_favorite/<int:course_id>/",
        views.add_to_favorites,
        name="add_to_favorites",
    ),
    path("my_favorites/", views.favorites, name="favorites"),
    path("my_courses/", views.my_training_courses, name="student_courses"),
]
