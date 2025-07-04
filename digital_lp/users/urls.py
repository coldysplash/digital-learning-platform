from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register_student/", views.register_student, name="register_student"),
    path("register_author/", views.register_author, name="register_author"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]
