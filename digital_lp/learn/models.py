from django.db import models

from users.models import User
from courses.models import Course
from course_construct.models import Task, Test, Lesson


class CourseProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    added_date = models.DateField(auto_now_add=True)
    progress_percentages = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ["student", "course"]


class LessonsProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    passed = models.BooleanField()

    class Meta:
        unique_together = ["student", "lesson"]


class FavoritesCourses(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["student", "course"]


class TestResults(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    pass_date = models.DateTimeField(auto_now_add=True)
    mark = models.BooleanField()

    class Meta:
        unique_together = ["student", "test"]


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
