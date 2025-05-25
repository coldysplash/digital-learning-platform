from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from courses.models import Course
from learn.models import CourseProgress


def redirect_if_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:profile")
        return view_func(request, *args, **kwargs)

    return wrapper


@redirect_if_authenticated
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


@redirect_if_authenticated
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


@redirect_if_authenticated
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
def profile(request, form=None):
    user = request.user
    form = form or UserProfileForm(instance=user)
    if user.is_author:
        author_courses = Course.objects.filter(author=user)
        return render(
            request,
            "users/author_profile.html",
            {"form": form, "courses": author_courses},
        )

    course_progress = CourseProgress.objects.filter(student=user)
    return render(
        request,
        "users/student_profile.html",
        {"form": form, "progress": course_progress},
    )


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
        return profile(request, form=form)
    else:
        form = UserProfileForm(instance=user)

    return render(request, "users/edit_profile.html", {"form": form})
