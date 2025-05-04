from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ValidationError

from courses.models import Course
from users.models import User


# Модель для отдельного модуля курса с уроками
class Module(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Модель для уроков
class Lesson(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ["module", "title"]
        ordering = ["order"]

    def __str__(self):
        return self.title


# Связующая модель для контента урока
class LessonContent(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    order = models.PositiveSmallIntegerField(default=0)  # Поле для сортировки

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Content for {self.lesson.title}"


# Модели для типов контента
class TextContent(models.Model):
    text = models.TextField()


class FileContent(models.Model):
    file = models.FileField(upload_to="lesson_files/%Y/%m/%d", blank=True)


class LinkContent(models.Model):
    url = models.URLField()


class ImageContent(models.Model):
    image = models.ImageField(upload_to="lesson_images/%Y/%m/%d", blank=True)


# Модели для реализации тестов
class Test(models.Model):
    title = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    passing_score = models.PositiveSmallIntegerField(blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)


class Questions(models.Model):
    question = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["test", "order"]
        ordering = ["order"]


class Answers(models.Model):
    answer = models.CharField(max_length=255)
    flag = models.BooleanField(default=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)


class TestResults(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    pass_date = models.DateTimeField(auto_now_add=True)
    mark = models.BooleanField()

    class Meta:
        unique_together = ["student", "test"]


# Модели для формы заданий
class Task(models.Model):
    title = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def clean(self):
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past.")


class TaskFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    solution = models.FileField(upload_to="task_solutions/%Y/%m/%d", blank=True)
    grade = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ["student", "task"]


class TaskComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task_feedback = models.ForeignKey(TaskFeedback, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = ["author", "task_feedback"]
