from django.test import TestCase

from .models import FavoritesCourses
from courses.models import Course, Category
from users.models import User


class FavoritesCoursesModelTest(TestCase):
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
            category=self.category,
            author=self.user,
        )
        self.favorite = FavoritesCourses.objects.create(
            student=self.user, course=self.course
        )

    def test_favorites_courses_creation(self):
        self.assertTrue(isinstance(self.favorite, FavoritesCourses))
        self.assertEqual(self.favorite.student, self.user)
        self.assertEqual(self.favorite.course, self.course)
