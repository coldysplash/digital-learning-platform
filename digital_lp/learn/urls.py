from django.urls import path

from . import views

app_name = "learn"

# learn profile data
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

# learn course
urlpatterns += [
    path("course/<int:course_id>/start", views.start_learn, name="start"),
    path("module/<int:pk>/", views.ModuleDetailView.as_view(), name="module"),
    path("lesson/<int:pk>/", views.LessonDetailView.as_view(), name="lesson"),
    path("test/<int:pk>/", views.TestDetailView.as_view(), name="test"),
]
