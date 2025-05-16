from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import transaction


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import *
from .forms import *
from users.views import author_required


class ConstructorCourseView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "construct/main.html"
    context_object_name = "module_list"

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs["pk"])
        return Module.objects.filter(course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs["pk"])
        context["course"] = course
        # Добавляем список всех уроков курса, отсортированных по модулю и порядку
        context["lessons"] = Lesson.objects.filter(module__course=course).order_by(
            "module__order", "order"
        )
        return context


# Module CRUD
class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = "modules/module.html"
    context_object_name = "module"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = self.object.lesson_set.all()
        return context


class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "modules/create.html"

    def form_valid(self, form):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        form.instance.course = course
        form.instance.order = course.module_set.count() + 1
        response = super().form_valid(form)
        messages.success(self.request, "Модуль успешно создан!")
        return response

    def get_success_url(self):
        return reverse_lazy("construct:main", kwargs={"pk": self.kwargs["course_id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, id=self.kwargs["course_id"])
        return context


class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "modules/form.html"

    def get_success_url(self):
        return reverse_lazy("construct:main", kwargs={"pk": self.object.course.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.object.course
        context["module"] = self.object
        return context


@login_required
@author_required
def module_delete(request, pk):
    module = get_object_or_404(Module, id=pk)
    course = module.course
    if request.method == "POST":
        module.delete()
        # Обновляем order для оставшихся модулей
        for i, mod in enumerate(course.module_set.all(), start=1):
            mod.order = i
            mod.save()
        messages.success(request, "Модуль удален!")
        return redirect("construct:main", pk=course.id)

    return render(
        request,
        "modules/delete.html",
        {"module": module, "course": course},
    )


# Lesson CRUD
class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/create.html"

    def form_valid(self, form):
        module = get_object_or_404(Module, id=self.kwargs["module_id"])
        count_lesson = Lesson.objects.filter(module=module).count()
        form.instance.order = count_lesson + 1
        form.instance.module = module
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("construct:module", kwargs={"pk": self.kwargs["module_id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module"] = get_object_or_404(Module, id=self.kwargs["module_id"])
        return context


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lessons/lesson.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем контент урока в контекст
        context["contents"] = self.object.contents.all()
        return context


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/form.html"

    def get_success_url(self):
        return reverse_lazy("construct:lesson", kwargs={"pk": self.object.pk})


@login_required
@author_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    module = lesson.module
    course = module.course
    if request.method == "POST":
        lesson.delete()
        # Обновляем order для оставшихся уроков
        for i, les in enumerate(lesson.module.lesson_set.all(), start=1):
            if les.order != i:
                les.order = i
                les.save()
        messages.success(request, "Урок удален!")
        return redirect("construct:main", pk=course.id)

    return render(
        request,
        "lessons/delete.html",
        {"lesson": lesson, "module": module},
    )


# Базовое представление для создания контента
class BaseContentCreateView(LoginRequiredMixin, CreateView):
    template_name = "lessons/content/create_form.html"

    def form_valid(self, form):
        content_object = form.save()
        lesson = Lesson.objects.get(id=self.kwargs["lesson_id"])
        content_type_obj = ContentType.objects.get_for_model(content_object)
        order = LessonContent.objects.filter(lesson=lesson).count() + 1
        LessonContent.objects.create(
            lesson=lesson,
            content_type=content_type_obj,
            object_id=content_object.id,
            order=order,
        )
        return redirect(reverse_lazy("construct:lesson", kwargs={"pk": lesson.id}))


# Представления для создания каждого типа контента
class TextContentCreateView(BaseContentCreateView):
    model = TextContent
    form_class = TextContentForm


class FileContentCreateView(BaseContentCreateView):
    model = FileContent
    form_class = FileContentForm


class LinkContentCreateView(BaseContentCreateView):
    model = LinkContent
    form_class = LinkContentForm


class ImageContentCreateView(BaseContentCreateView):
    model = ImageContent
    form_class = ImageContentForm


# Представление для редактирования контента
class ContentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lessons/content/edit_form.html"

    def get_object(self):
        lesson_content = LessonContent.objects.get(id=self.kwargs["pk"])
        return lesson_content.content_object

    def get_form_class(self):
        lesson_content = LessonContent.objects.get(id=self.kwargs["pk"])
        content_type = lesson_content.content_type.model
        form_classes = {
            "textcontent": TextContentForm,
            "filecontent": FileContentForm,
            "linkcontent": LinkContentForm,
            "imagecontent": ImageContentForm,
        }
        return form_classes[content_type]

    def form_valid(self, form):
        form.save()
        return redirect(
            reverse_lazy("construct:lesson", kwargs={"pk": self.kwargs["lesson_id"]})
        )


# Представление для удаления контента
class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = LessonContent
    template_name = "lessons/content/confirm_delete.html"

    def post(self, request, *args, **kwargs):
        lesson_content = self.get_object()
        content_object = lesson_content.content_object
        with transaction.atomic():
            lesson_content.delete()
            content_object.delete()
            remaining_contents = LessonContent.objects.filter(
                lesson=self.kwargs["lesson_id"]
            ).order_by("order")
            for index, content in enumerate(remaining_contents, start=1):
                content.order = index
                content.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("construct:lesson", kwargs={"pk": self.kwargs["lesson_id"]})
