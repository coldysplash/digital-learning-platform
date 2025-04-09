from django.test import TestCase, Client
from django.urls import reverse

from ..models import User


class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_student_url = reverse("users:register_student")
        self.register_author_url = reverse("users:register_author")
        self.login_url = reverse("users:user_login")

    def test_register_student_view(self):
        """Тест регистрации студента"""
        response = self.client.post(
            self.register_student_url,
            {
                "email": "student@example.com",
                "password1": "studentpassword123",
                "password2": "studentpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="student@example.com").exists())

    def test_register_author_view(self):
        """Тест регистрации автора"""
        response = self.client.post(
            self.register_author_url,
            {
                "email": "author@example.com",
                "password1": "authorpassword123",
                "password2": "authorpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="author@example.com")
        self.assertTrue(user.is_author)

    def test_login_view(self):
        """Тест входа пользователя"""
        User.objects.create_user(email="test@example.com", password="testpassword")
        response = self.client.post(
            self.login_url, {"email": "test@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
