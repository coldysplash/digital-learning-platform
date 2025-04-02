from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name = "course_category"
        verbose_name_plural = "course_categories"

    def __str__(self):
        return self.name

    def get_course_count(self):
        return Course.objects.filter(category=self).count()


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    """author_id = models.ForeignKey(User, on_delete=models.CASCADE)"""
    image = models.ImageField(upload_to="media/course_images/%Y/%m/%d", blank=True)
    verified = models.BooleanField(default=False)
    pub_date = models.DateField(blank=True, null=True)
    available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
