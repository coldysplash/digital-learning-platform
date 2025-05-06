from django.test import TestCase
from .models import Course, Category

from users.models import User


class CourseModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="This is a test category",
        )
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.course = Course.objects.create(
            name="Test Course",
            description="This is a test course",
            author=self.user,
            category=self.category,
        )

    def test_course_creation(self):
        self.assertTrue(isinstance(self.course, Course))
        self.assertEqual(self.course.__str__(), self.course.name)

    def test_course_fields(self):
        self.assertEqual(self.course.name, "Test Course")
        self.assertEqual(self.course.description, "This is a test course")
        self.assertEqual(self.course.author, self.user)
        self.assertEqual(self.course.category, self.category)
