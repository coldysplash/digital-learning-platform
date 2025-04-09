from django.test import TestCase

from ..models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        """Тест создания обычного пользователя"""
        email = "test@example.com"
        password = "testpassword"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        email = "admin@example.com"
        password = "adminpassword"
        admin_user = User.objects.create_superuser(email=email, password=password)
        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
