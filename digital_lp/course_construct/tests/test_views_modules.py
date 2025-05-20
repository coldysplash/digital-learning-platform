from django.test import TestCase, Client
from django.urls import reverse

from users.models import User
from courses.models import Course, Category
from ..models import Module
from ..forms import ModuleForm


class ModuleEditViewTest(TestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="testpass", is_author=True
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
            author=self.user,
            category=self.category,
            verified=False,
            available=False,
        )
        # Создаём несколько модулей
        self.module1 = Module.objects.create(
            name="Module 1", description="Description 1", course=self.course, order=1
        )
        self.module2 = Module.objects.create(
            name="Module 2", description="Description 2", course=self.course, order=2
        )
        self.module3 = Module.objects.create(
            name="Module 3", description="Description 3", course=self.course, order=3
        )
        # Инициализируем тестовый клиент
        self.client = Client()
        # URL для редактирования модуля
        self.url = reverse("construct:module_edit", kwargs={"pk": self.module1.id})

    def test_module_edit_get_authenticated(self):
        # Проверяем GET-запрос для авторизованного пользователя
        self.client.login(email="testuser@gmail.com", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "modules/form.html")
        self.assertIsInstance(response.context["form"], ModuleForm)
        self.assertEqual(response.context["module"], self.module1)
        self.assertEqual(response.context["course"], self.course)

    def test_module_edit_post_valid_form(self):
        # Проверяем POST-запрос с валидной формой
        self.client.login(email="testuser@gmail.com", password="testpass")
        post_data = {
            "name": "Updated Module",
            "description": "Updated Description",
        }
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 302)
        # Проверяем перенаправление на construct:main
        self.assertRedirects(
            response, reverse("construct:main", kwargs={"course_id": self.course.id})
        )
        # Проверяем, что данные модуля обновились
        self.module1.refresh_from_db()
        self.assertEqual(self.module1.name, "Updated Module")
        self.assertEqual(self.module1.description, "Updated Description")

    def test_module_edit_nonexistent_module(self):
        # Проверяем доступ к несуществующему модулю
        self.client.login(email="testuser@gmail.com", password="testpass")
        nonexistent_url = reverse("construct:module_edit", kwargs={"pk": 999})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_module_and_update_order(self):
        # Проверяем начальные значения order
        initial_orders = [
            mod.order for mod in Module.objects.filter(course=self.course)
        ]
        self.assertEqual(initial_orders, [1, 2, 3])

        # Выполняем DELETE-запрос для удаления второго модуля
        url = reverse("construct:module_delete", kwargs={"pk": self.module2.id})
        self.client.login(email="testuser@gmail.com", password="testpass")
        response = self.client.post(url)

        # Проверяем, что order оставшихся модулей обновился
        updated_modules = Module.objects.filter(course=self.course).order_by("order")
        updated_orders = [mod.order for mod in updated_modules]
        self.assertEqual(
            updated_orders, [1, 2], "Order значений должен быть [1, 2] после удаления"
        )

        # Проверяем имена оставшихся модулей
        updated_names = [mod.name for mod in updated_modules]
        self.assertEqual(updated_names, ["Module 1", "Module 3"])

        # Проверяем перенаправление
        self.assertRedirects(
            response, reverse("construct:main", kwargs={"course_id": self.course.id})
        )
