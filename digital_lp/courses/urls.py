from django.urls import path

from .views import CatalogView, CourseDetailView

app_name = "courses"

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog"),
    path("course/<int:pk>", CourseDetailView.as_view(), name="course_detail_view"),
]
