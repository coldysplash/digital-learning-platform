from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from django.db import transaction

from .models import *


class AuthorRequiredMixin(AccessMixin):
    """Mixin для проверки, является ли пользователь автором курса."""

    # Словарь для получения курса по параметрам URL
    course_getters = {
        "course_id": lambda self: get_object_or_404(
            Course, id=self.kwargs["course_id"]
        ),
        "module_id": lambda self: get_object_or_404(
            Module, id=self.kwargs["module_id"]
        ).course,
        "lesson_id": lambda self: get_object_or_404(
            Lesson, id=self.kwargs["lesson_id"]
        ).module.course,
        "test_id": lambda self: get_object_or_404(
            Test, id=self.kwargs["test_id"]
        ).module.course,
        "question_id": lambda self: get_object_or_404(
            Questions, id=self.kwargs["question_id"]
        ).test.module.course,
        "pk": lambda self: self._get_course_from_pk(),
    }

    def _get_course_from_pk(self):
        """Вспомогательный метод для получения курса по pk."""
        obj = self.get_object()
        if isinstance(obj, Course):
            return obj
        elif isinstance(obj, Module):
            return obj.course
        elif isinstance(obj, Lesson):
            return obj.module.course
        elif isinstance(obj, Test):
            return obj.module.course
        elif isinstance(obj, Questions):
            return obj.test.module.course
        elif isinstance(obj, Answers):
            return obj.question.test.module.course
        return None

    def dispatch(self, request, *args, **kwargs):
        course = None
        # Проверяем наличие параметров в kwargs и получаем курс
        for param, getter in self.course_getters.items():
            if param in self.kwargs:
                course = getter(self)
                break

        # Если курс не найден, возвращаем ошибку доступа
        if not course:
            return self.handle_no_permission()

        # Проверяем, является ли пользователь автором курса
        if course.author != request.user:
            return self.handle_no_permission()

        # Если всё в порядке, продолжаем выполнение
        return super().dispatch(request, *args, **kwargs)


def delete_module_in_course(object: Module, course):
    with transaction.atomic():
        object.delete()
        updated_modules = []
        for index, mod in enumerate(course.module_set.all().order_by("order"), start=1):
            if mod.order != index:
                mod.order = index
                updated_modules.append(mod)

        if updated_modules:
            Module.objects.bulk_update(updated_modules, ["order"])


def delete_item_in_module(object):
    with transaction.atomic():
        object.delete()
        items = type(object).objects.filter(module=object.module).order_by("order")
        updated_items = []
        for index, item in enumerate(items, start=1):
            if item.order != index:
                item.order = index
                updated_items.append(item)

        if updated_items:
            type(object).objects.bulk_update(updated_items, ["order"])


def delete_item_in_test(object):
    with transaction.atomic():
        object.delete()
        items = type(object).objects.filter(test=object.test).order_by("order")
        updated_items = []
        for index, item in enumerate(items, start=1):
            if item.order != index:
                item.order = index
                item.save()
                updated_items.append(item)

        if updated_items:
            type(object).objects.bulk_update(updated_items, ["order"])
