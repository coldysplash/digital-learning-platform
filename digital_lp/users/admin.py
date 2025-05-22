from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "is_staff",
        "is_author",
    )
    search_fields = ("email", "name")
    list_filter = ("is_staff", "is_active", "is_author")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("name", "image")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_author", "is_staff", "is_superuser")},
        ),
    )

    add_fieldets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_active",
                "is_author",
                "is_staff",
                "is_superuser",
            ),
        },
    )
