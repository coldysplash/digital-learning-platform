from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register_student/", views.register_student, name="register_student"),
    path("register_author/", views.register_author, name="register_author"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("student_profile/", views.profile_student, name="student_profile"),
    path("author_profile/", views.profile_author, name="author_profile"),
]
