from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path(
        "course/<int:pk>", views.CourseDetailView.as_view(), name="course_detail_view"
    ),
    path("course/create/", views.course_create, name="create"),
]
