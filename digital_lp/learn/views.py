from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


from .models import CourseProgress, FavoritesCourses, LessonsProgress
from courses.models import Course
from course_construct.views import get_sidebar_context
from course_construct.models import Module, Lesson, Test, Questions
from .utils import StudentRequiredMixin


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    if request.method == "POST":
        if not CourseProgress.objects.filter(student=user, course=course).exists():
            CourseProgress.objects.create(student=user, course=course)
        else:
            redirect("courses:course_detail_view", pk=course_id)

    return redirect("courses:course_detail_view", pk=course_id)


@login_required
def add_to_favorites(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    if request.method == "POST":
        if not FavoritesCourses.objects.filter(student=user, course=course).exists():
            FavoritesCourses.objects.create(student=user, course=course)
        else:
            redirect("courses:course_detail_view", pk=course_id)

    return redirect("courses:course_detail_view", pk=course_id)


@login_required
def favorites(request):
    user = request.user
    fav_courses = FavoritesCourses.objects.filter(student=user)
    return render(
        request,
        "learn/favorites.html",
        {"favorite_courses": fav_courses},
    )


@login_required
def my_training_courses(request):
    user = request.user
    student_courses = CourseProgress.objects.filter(student=user)
    return render(
        request,
        "learn/my_courses.html",
        {"student_courses": student_courses},
    )


@login_required
def start_learn(request, course_id):
    context = get_sidebar_context(course_id)
    return render(request, "learn/start.html", context)


class ModuleDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    model = Module
    template_name = "learn/modules/module.html"
    context_object_name = "module"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_sidebar_context(self.object.course.id))
        return context


class LessonDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    model = Lesson
    template_name = "learn/lessons/lesson.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contents"] = self.object.contents.all()
        context["progress"] = LessonsProgress.objects.get(
            lesson=self.object.id, student=self.request.user
        )
        context.update(get_sidebar_context(self.object.module.course.id))
        return context


class TestDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    model = Test
    template_name = "learn/tests/test.html"
    context_object_name = "test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_sidebar_context(self.object.module.course.id))
        context["questions"] = Questions.objects.filter(test=self.object).order_by(
            "order"
        )
        return context


class CompleteLessonView(LoginRequiredMixin, View):
    """
    View для отметки урока как пройденного студентом.
    """

    def post(self, request, lesson_id):
        # Получаем урок или возвращаем 404, если он не найден
        lesson = get_object_or_404(Lesson, id=lesson_id)

        # Получаем или создаем запись в LessonsProgress
        progress, created = LessonsProgress.objects.get_or_create(
            student=request.user, lesson=lesson, defaults={"passed": True}
        )

        # Если запись уже существует, обновляем поле passed
        if not created:
            progress.passed = True
            progress.save()

        # Перенаправляем на страницу урока
        return redirect("learn:lesson", pk=lesson.id)
