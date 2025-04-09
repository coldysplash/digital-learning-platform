from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register_student(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:user_login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register_student.html", {"form": form})


def register_author(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_author = True
            user.save()
            login(request, user)
            return redirect("users:user_login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register_author.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_author:
                    return redirect("users:author_profile")
                else:
                    return redirect("users:student_profile")
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


@login_required(login_url="/users/login")
def user_logout(request):
    logout(request)
    return redirect("users:user_login")


@login_required
def profile_author(request):
    if not request.user.is_author:
        return redirect("users:student_profile")

    return render(request, "users/author_profile.html")


@login_required
def profile_student(request):
    if request.user.is_author:
        return redirect("users:author_profile")

    return render(request, "users/student_profile.html")
