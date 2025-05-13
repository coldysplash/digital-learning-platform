from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from courses.models import Course, Category
from ..models import Module, Lesson
from users.models import User


class LessonViewsTests(TestCase):
    def setUp(self):
        # Создаем пользователей
        self.client = Client()
        self.author = User.objects.create_user(
            email="author@test.com", password="testpass123", is_author=True
        )
        self.non_author = User.objects.create_user(
            email="non_author@test.com", password="testpass123", is_author=False
        )
        # Создаём тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="Test Category Description",
        )
        # Создаём тестовый курс
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            author=self.author,
            category=self.category,
            verified=False,
            available=False,
        )
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

    def test_lesson_create_view_author_get(self):
        # Проверка GET-запроса для автора
        self.client.login(email="author@test.com", password="testpass123")
        response = self.client.get(
            reverse("construct:lesson_create", kwargs={"module_id": self.module.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lessons/create.html")
        self.assertIn("module", response.context)
        self.assertEqual(response.context["module"], self.module)

    def test_lesson_create_view_author_post(self):
        # Проверка создания урока
        self.client.login(email="author@test.com", password="testpass123")
        lesson_data = {
            "title": "New Lesson",
            "description": "New lesson description",
            "module": self.module.id,
        }
        response = self.client.post(
            reverse("construct:lesson_create", kwargs={"module_id": self.module.id}),
            lesson_data,
        )
        self.assertEqual(response.status_code, 302)

        new_lesson = Lesson.objects.get(title="New Lesson")
        self.assertEqual(new_lesson.order, 2)  # После существующего урока с order=1
        self.assertEqual(new_lesson.module, self.module)

    def test_lesson_detail_view_author(self):
        # Проверка отображения урока
        self.client.login(email="author@test.com", password="testpass123")
        response = self.client.get(
            reverse("construct:lesson", kwargs={"pk": self.lesson.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lessons/lesson.html")
        self.assertEqual(response.context["lesson"], self.lesson)

    def test_lesson_update_view_author_post(self):
        # Проверка обновления урока
        self.client.login(email="author@test.com", password="testpass123")
        updated_data = {
            "title": "Updated Lesson",
            "description": "Updated description",
            "module": self.module.id,
        }
        response = self.client.post(
            reverse("construct:lesson_edit", kwargs={"pk": self.lesson.id}),
            updated_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("construct:lesson", kwargs={"pk": self.lesson.id})
        )
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_lesson_delete_view_author_get(self):
        # Проверка GET-запроса для удаления
        self.client.login(email="author@test.com", password="testpass123")
        response = self.client.get(
            reverse("construct:lesson_delete", kwargs={"pk": self.lesson.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lessons/delete.html")
        self.assertIn("lesson", response.context)

    def test_lesson_delete_view_author_post(self):
        # Проверка удаления урока
        self.client.login(email="author@test.com", password="testpass123")
        # Создаем второй урок для проверки обновления порядка
        second_lesson = Lesson.objects.create(
            title="Second Lesson",
            description="Second lesson description",
            module=self.module,
            order=2,
        )
        response = self.client.post(
            reverse("construct:lesson_delete", kwargs={"pk": self.lesson.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("construct:main", kwargs={"pk": self.course.id})
        )
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
        second_lesson.refresh_from_db()
        self.assertEqual(second_lesson.order, 1)  # Порядок должен обновиться
