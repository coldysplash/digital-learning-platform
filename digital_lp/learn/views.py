from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render

from .models import CourseProgress, FavoritesCourses
from courses.models import Course


@login_required(login_url="/users/login")
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    if request.method == "POST":
        if not CourseProgress.objects.filter(student=user, course=course).exists():
            CourseProgress.objects.create(student=user, course=course)
        else:
            redirect("courses:course_detail_view", pk=course_id)

    return redirect("courses:course_detail_view", pk=course_id)


@login_required(login_url="/users/login")
def add_to_favorites(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    if request.method == "POST":
        if not FavoritesCourses.objects.filter(student=user, course=course).exists():
            FavoritesCourses.objects.create(student=user, course=course)
        else:
            redirect("courses:course_detail_view", pk=course_id)

    return redirect("courses:course_detail_view", pk=course_id)


@login_required(login_url="/users/login")
def favorites(request):
    user = request.user
    fav_courses = FavoritesCourses.objects.filter(student=user)
    return render(
        request,
        "learn/favorites.html",
        {"favorite_courses": fav_courses},
    )


@login_required(login_url="/users/login")
def my_training_courses(request):
    user = request.user
    student_courses = CourseProgress.objects.filter(student=user)
    return render(
        request,
        "learn/my_courses.html",
        {"student_courses": student_courses},
    )
