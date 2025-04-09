from django.test import TestCase

from ..forms import UserRegistrationForm, UserLoginForm
from ..models import User


class UserRegistrationFormTests(TestCase):
    def test_valid_form(self):
        """Тест валидной формы регистрации"""
        form_data = {
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """Тест несовпадения паролей"""
        form_data = {
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "differentpassword",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_short_password(self):
        """Тест короткого пароля"""
        form_data = {
            "email": "test@example.com",
            "password1": "short",
            "password2": "short",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password1"], ["Minimum 8 characters."])


class UserLoginFormTests(TestCase):
    def test_valid_login_form(self):
        """Тест валидной формы входа"""
        # Создаем пользователя с указанным email и паролем
        User.objects.create_user(email="test@example.com", password="testpassword")

        form_data = {"email": "test@example.com", "password": "testpassword"}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_empty_password(self):
        """Тест невалидной формы входа (пустой пароль)"""
        form_data = {"email": "test@example.com", "password": ""}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_login_form_incorrect_password(self):
        """Тест невалидной формы входа (неверный пароль)"""
        User.objects.create_user(email="test@example.com", password="testpassword")
        form_data = {"email": "test@example.com", "password": "wrongpassword"}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_login_form_nonexistent_user(self):
        """Тест невалидной формы входа (несуществующий пользователь)"""
        form_data = {"email": "nonexistent@example.com", "password": "testpassword"}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
