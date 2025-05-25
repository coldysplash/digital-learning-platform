from django import forms

from .models import *


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


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description", "passing_score"]
        labels = {
            "title": "Название теста",
            "description": "Описание",
            "passing_score": "Прохдной балл для теста (можно установаить позже)",
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ["question"]
        labels = {
            "question": "Вопрос",
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ["answer", "flag"]
        labels = {"answer": "Ответ", "flag": "Правильный"}
