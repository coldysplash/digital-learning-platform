from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from ..models import (
    Lesson,
    LessonContent,
    TextContent,
    FileContent,
    LinkContent,
    ImageContent,
    Module,
)
from users.models import User
from courses.models import Course, Category


class ContentViewsTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            email="test@example.com", password="password"
        )
        # Создаем категорию
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test Category Description",
        )
        # Создаем курс
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            author=self.user,
            category=self.category,
            verified=False,
            available=False,
        )
        # Создаем модуль
        self.module = Module.objects.create(
            name="Test Module", description="Module description", course=self.course
        )
        # Создаем урок
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson description",
            module=self.module,
            order=1,
        )
        # Создаем клиента
        self.client = Client()
        # Логиним пользователя
        self.client.login(email="test@example.com", password="password")

    def test_text_content_create(self):
        """Тест создания текстового контента"""
        url = reverse("construct:add_text", kwargs={"lesson_id": self.lesson.id})
        data = {"text": "Test text content"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Проверяем перенаправление
        text_content = TextContent.objects.get(text="Test text content")
        lesson_content = LessonContent.objects.get(
            lesson=self.lesson,
            content_type=ContentType.objects.get_for_model(TextContent),
            object_id=text_content.id,
        )
        self.assertEqual(lesson_content.order, 1)  # Проверяем порядок

    def test_link_content_create(self):
        """Тест создания контента-ссылки"""
        url = reverse("construct:add_link", kwargs={"lesson_id": self.lesson.id})
        data = {"url": "https://example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        link_content = LinkContent.objects.get(url="https://example.com")
        lesson_content = LessonContent.objects.get(
            lesson=self.lesson,
            content_type=ContentType.objects.get_for_model(LinkContent),
            object_id=link_content.id,
        )
        self.assertEqual(lesson_content.order, 1)

    def test_content_update(self):
        """Тест редактирования контента"""
        text_content = TextContent.objects.create(text="Initial text")
        lesson_content = LessonContent.objects.create(
            lesson=self.lesson,
            content_type=ContentType.objects.get_for_model(TextContent),
            object_id=text_content.id,
            order=1,
        )
        url = reverse(
            "construct:content_edit",
            kwargs={"lesson_id": self.lesson.id, "pk": lesson_content.id},
        )
        data = {"text": "Updated text"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        text_content.refresh_from_db()
        self.assertEqual(text_content.text, "Updated text")

    def test_content_delete(self):
        """Тест удаления контента и обновления порядка"""
        text_content1 = TextContent.objects.create(text="Text 1")
        lesson_content1 = LessonContent.objects.create(
            lesson=self.lesson,
            content_type=ContentType.objects.get_for_model(TextContent),
            object_id=text_content1.id,
            order=1,
        )
        text_content2 = TextContent.objects.create(text="Text 2")
        lesson_content2 = LessonContent.objects.create(
            lesson=self.lesson,
            content_type=ContentType.objects.get_for_model(TextContent),
            object_id=text_content2.id,
            order=2,
        )
        url = reverse(
            "construct:content_delete",
            kwargs={"lesson_id": self.lesson.id, "pk": lesson_content1.id},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(LessonContent.DoesNotExist):
            LessonContent.objects.get(id=lesson_content1.id)
        with self.assertRaises(TextContent.DoesNotExist):
            TextContent.objects.get(id=text_content1.id)
        lesson_content2.refresh_from_db()
        self.assertEqual(lesson_content2.order, 1)

    def test_unauthorized_access(self):
        """Тест доступа неавторизованного пользователя"""
        self.client.logout()
        url = reverse("construct:add_text", kwargs={"lesson_id": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа
