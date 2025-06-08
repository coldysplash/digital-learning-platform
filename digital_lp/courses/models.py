from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name = "course_category"
        verbose_name_plural = "course_categories"

    def __str__(self):
        return self.name

    def get_course_count(self):
        return Course.objects.filter(category=self, available=True).count()


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="course_images/%Y/%m/%d", blank=True)
    verified = models.BooleanField(default=False)
    pub_date = models.DateField(blank=True, null=True)
    available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.name

    def delete(self):
        self.image.delete()
        super().delete()
