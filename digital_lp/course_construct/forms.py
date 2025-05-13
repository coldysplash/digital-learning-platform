from django import forms
from django.core.exceptions import ValidationError

from .models import Module, Lesson, TextContent, FileContent, LinkContent, ImageContent


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["name", "description"]
        labels = {
            "name": "Название модуля",
            "description": "Описание",
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description"]
        labels = {
            "title": "Название урока",
            "description": "Описание",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "module": forms.HiddenInput(),  # Поле module скрыто, так как передается через URL
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        module = cleaned_data.get("module")

        if title and module:
            # Проверяем, существует ли урок с таким названием в данном модуле
            existing_lesson = Lesson.objects.filter(title=title, module=module).exclude(
                pk=self.instance.pk if self.instance else None
            )

            if existing_lesson.exists():
                self.add_error(
                    "title", f"Урок с названием '{title}' уже существует в этом модуле."
                )

        return cleaned_data


class TextContentForm(forms.ModelForm):
    class Meta:
        model = TextContent
        fields = ["text"]


class FileContentForm(forms.ModelForm):
    class Meta:
        model = FileContent
        fields = ["file"]


class LinkContentForm(forms.ModelForm):
    class Meta:
        model = LinkContent
        fields = ["url"]


class ImageContentForm(forms.ModelForm):
    class Meta:
        model = ImageContent
        fields = ["image"]
