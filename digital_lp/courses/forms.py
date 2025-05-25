from django import forms
from django.core.exceptions import ValidationError
import os

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description", "image", "category"]
        labels = {
            "name": "Название курса",
            "description": "Описание",
            "image": "Изображение курса",
            "category": "Категория",
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) > 255:
            raise ValidationError("Название курса не может превышать 255 символов")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description) < 10:
            self.add_error(
                "description", "Описание должно содержать минимум 10 символов"
            )
        return description

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # Проверка размера файла (ограничим до 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5MB")

            # Проверка формата изображения
            valid_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Допустимые форматы изображения: JPG, JPEG, PNG")
        return image
