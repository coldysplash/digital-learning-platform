from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Module, Course
from .forms import ModuleForm
from users.views import author_required


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        course = self.get_course()
        return course.author == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden("You are not authorized to perform this action.")

    def get_course(self):
        if hasattr(self, "object") and self.object:
            return self.object.course
        if "pk" in self.kwargs:
            module = get_object_or_404(Module, id=self.kwargs["pk"])
            return module.course
        if "course_id" in self.kwargs:
            return get_object_or_404(Course, id=self.kwargs["course_id"])
        raise Http404("Course not found")


class ModuleListView(LoginRequiredMixin, AuthorRequiredMixin, ListView):
    model = Module
    template_name = "construct/main.html"
    context_object_name = "module_list"

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        return Module.objects.filter(course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, id=self.kwargs["course_id"])
        return context


class ModuleDetailView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    model = Module
    template_name = "modules/module.html"
    context_object_name = "module"


class ModuleCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
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
    template_name = "modules/form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Модуль сохранен!")
        return response

    def get_success_url(self):
        return reverse_lazy(
            "construct:main", kwargs={"course_id": self.object.course.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.object.course
        context["module"] = self.object
        return context


@login_required
@author_required
def module_delete(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course
    if request.method == "POST":
        module.delete()
        # Обновляем order для оставшихся модулей
        for i, mod in enumerate(course.module_set.all(), start=1):
            mod.order = i
            mod.save()
        messages.success(request, "Модуль удален!")
        return redirect("construct:main", course_id=course.id)

    return render(
        request,
        "modules/delete.html",
        {"module": module, "course": course},
    )
