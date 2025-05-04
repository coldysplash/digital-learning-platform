from django.db import models

from users.models import User
from courses.models import Course


class CourseProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    added_date = models.DateField(auto_now_add=True)
    progress_percentages = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ["student", "course"]


class FavoritesCourses(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["student", "course"]
