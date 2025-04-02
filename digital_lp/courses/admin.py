from django.contrib import admin

from .models import Course, Category


@admin.register(Category)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Course)
class CourseItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "available",
        "verified",
        "pub_date",
    )
    list_filter = ("available", "category")
