from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from functools import wraps
from django.http import Http404

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from courses.models import Course


def is_authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:profile")
        return view_func(request, *args, **kwargs)

    return wrapper


def author_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_author:
            raise Http404("You can't create a course, because you're not the author.")
        return view_func(request, *args, **kwargs)

    return wrapper


@is_authenticated_user
def register_student(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("users:user_login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register_student.html", {"form": form})


@is_authenticated_user
def register_author(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_author = True
            user.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("users:user_login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register_author.html", {"form": form})


@is_authenticated_user
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("users:profile")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("users:user_login")


@login_required
def profile(request):
    user = request.user
    if user.is_author:
        form = UserProfileForm(instance=user)
        author_courses = Course.objects.filter(author=user)
        return render(
            request,
            "users/author_profile.html",
            {"form": form, "courses": author_courses},
        )
    else:
        form = UserProfileForm(instance=user)
        return render(
            request,
            "users/student_profile.html",
            {"form": form},
        )
