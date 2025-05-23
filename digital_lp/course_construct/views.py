from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .utils import (
    delete_item_in_module,
    delete_item_in_test,
    delete_module_in_course,
    AuthorRequiredMixin,
)
from .models import *
from .forms import *
from learn.models import CourseProgress


def get_sidebar_context(course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        "course": course,
        "module_list": Module.objects.filter(course=course).select_related("course"),
        "lessons": Lesson.objects.filter(module__course=course)
        .order_by("module__order", "order")
        .select_related("module"),
        "tests": Test.objects.filter(module__course=course)
        .order_by("module__order", "order")
        .select_related("module"),
    }
    return context


class ConstructorCourseView(LoginRequiredMixin, AuthorRequiredMixin, ListView):
    model = Module
    template_name = "construct/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        context["students_count"] = CourseProgress.objects.filter(course=course).count()
        context.update(get_sidebar_context(course.id))
        return context


# Module CRUD
class ModuleDetailView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    model = Module
    template_name = "construct/modules/module.html"
    context_object_name = "module"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_sidebar_context(self.object.course.id))
        return context


class ModuleCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "construct/modules/create.html"

    def form_valid(self, form):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        form.instance.course = course
        form.instance.order = course.module_set.count() + 1
        response = super().form_valid(form)
        messages.success(self.request, "Модуль успешно создан!")
        return response

    def get_success_url(self):
        return reverse_lazy(
            "construct:main", kwargs={"course_id": self.kwargs["course_id"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, id=self.kwargs["course_id"])
        return context


class ModuleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "construct/modules/form.html"

    def get_success_url(self):
        return reverse_lazy("construct:module", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module"] = self.object
        return context


@login_required
def module_delete(request, pk):
    module = get_object_or_404(Module, id=pk)
    course = module.course
    if request.method == "POST":
        delete_module_in_course(module, course)
        return redirect("construct:main", course_id=course.id)

    return render(
        request,
        "construct/modules/delete.html",
        {"module": module, "course": course},
    )


# Lesson CRUD
class LessonCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "construct/lessons/create.html"

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


class LessonDetailView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    model = Lesson
    template_name = "construct/lessons/lesson.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["contents"] = self.object.contents.all()
        context.update(get_sidebar_context(self.object.module.course.id))
        return context


class LessonUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "construct/lessons/form.html"

    def get_success_url(self):
        return reverse_lazy("construct:lesson", kwargs={"pk": self.object.pk})


@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    module = lesson.module
    course = module.course
    if request.method == "POST":
        delete_item_in_module(lesson)
        return redirect("construct:main", course_id=course.id)

    return render(
        request,
        "construct/lessons/delete.html",
        {"lesson": lesson, "module": module},
    )


# Базовое представление для создания контента
class BaseContentCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    template_name = "construct/lessons/content/create_form.html"

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
class ContentUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    template_name = "construct/lessons/content/edit_form.html"

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
class ContentDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = LessonContent
    template_name = "construct/lessons/content/confirm_delete.html"

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
                if content.order != index:
                    content.order = index
                    content.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("construct:lesson", kwargs={"pk": self.kwargs["lesson_id"]})


# Tests CRUD
class TestCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = "construct/tests/create.html"

    def form_valid(self, form):
        module = get_object_or_404(Module, id=self.kwargs["module_id"])
        count_test = Test.objects.filter(module=module).count()
        form.instance.order = count_test + 1
        form.instance.module = module
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("construct:module", kwargs={"pk": self.kwargs["module_id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module"] = get_object_or_404(Module, id=self.kwargs["module_id"])
        return context


class TestDetailView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    model = Test
    template_name = "construct/tests/test_detail.html"
    context_object_name = "test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Questions.objects.filter(test=self.object).order_by(
            "order"
        )
        context.update(get_sidebar_context(self.object.module.course.id))
        return context


class TestUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Test
    form_class = TestForm
    template_name = "construct/tests/form.html"

    def get_success_url(self):
        return reverse_lazy("construct:test_detail", kwargs={"pk": self.object.pk})


@login_required
def test_delete(request, pk):
    test = get_object_or_404(Test, id=pk)
    module = test.module
    if request.method == "POST":
        delete_item_in_module(test)
        return redirect("construct:module", pk=module.id)

    return render(
        request,
        "construct/tests/confirm_delete.html",
        {"test": test, "module": module},
    )


# Questions CRUD
class QuestionCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Questions
    form_class = QuestionForm
    template_name = "construct/tests/questions/create.html"

    def form_valid(self, form):
        test = get_object_or_404(Test, id=self.kwargs["test_id"])
        count_quest = Questions.objects.filter(test=test).count()
        form.instance.order = count_quest + 1
        form.instance.test = test
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "construct:test_detail", kwargs={"pk": self.kwargs["test_id"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["test"] = get_object_or_404(Test, id=self.kwargs["test_id"])
        return context


class QuestionDetailView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    model = Questions
    template_name = "construct/tests/questions/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["test"] = get_object_or_404(Test, id=self.object.test.id)
        context["answers"] = Answers.objects.filter(question=self.object)
        return context


class QuestionUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Questions
    form_class = QuestionForm
    template_name = "construct/tests/questions/form.html"

    def get_success_url(self):
        return reverse_lazy("construct:test_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.object
        context["test"] = self.object.test
        return context


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Questions, id=pk)
    if request.method == "POST":
        delete_item_in_test(question)
        return redirect("construct:test_detail", pk=question.test.id)


class AnswerCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Answers
    form_class = AnswerForm
    template_name = "construct/tests/answers/create.html"

    def form_valid(self, form):
        form.instance.question = get_object_or_404(
            Questions, id=self.kwargs["question_id"]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "construct:question_detail",
            kwargs={"pk": self.kwargs["question_id"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = get_object_or_404(
            Questions, id=self.kwargs["question_id"]
        )
        return context


class AnswerUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Answers
    form_class = AnswerForm
    template_name = "construct/tests/answers/form.html"
    context_object_name = "answer"

    def get_success_url(self):
        question = self.object.question
        return reverse_lazy(
            "construct:question_detail",
            kwargs={"pk": question.id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.object.question
        return context


class AnswerDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Answers

    def get_success_url(self):
        return reverse_lazy(
            "construct:question_detail",
            kwargs={"pk": self.object.question.id},
        )
