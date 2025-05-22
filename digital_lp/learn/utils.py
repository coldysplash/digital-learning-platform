from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404


from course_construct.models import *
from .models import CourseProgress


class StudentRequiredMixin(AccessMixin):
    """Mixin для проверки, является ли пользователь студентом записанным на курс."""

    # Словарь для получения курса по параметрам URL
    course_getters = {
        "course_id": lambda self: get_object_or_404(
            Course, id=self.kwargs["course_id"]
        ),
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

        # Проверяем, является ли пользователь студентом курса
        course_progress = CourseProgress.objects.filter(
            course=course, student=request.user
        )
        if not course_progress:
            return self.handle_no_permission()

        # Если всё в порядке, продолжаем выполнение
        return super().dispatch(request, *args, **kwargs)
