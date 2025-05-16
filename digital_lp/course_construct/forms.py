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
