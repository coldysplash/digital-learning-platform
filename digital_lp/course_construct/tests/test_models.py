from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import *
from courses.models import Course, Category


class ModuleModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )

    def test_create_module(self):
        module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )
        self.assertEqual(module.name, "Test Module")
        self.assertEqual(module.course, self.course)


class LessonModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )

    def test_create_lesson(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson Description",
            module=self.module,
            order=1,
        )
        self.assertEqual(lesson.title, "Test Lesson")
        self.assertEqual(lesson.module, self.module)

    def test_unique_title_per_module(self):
        Lesson.objects.create(
            title="Unique Lesson",
            description="Description",
            module=self.module,
            order=1,
        )
        with self.assertRaises(Exception):
            Lesson.objects.create(
                title="Unique Lesson",
                description="Another Description",
                module=self.module,
                order=2,
            )


class LessonContentModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson Description",
            module=self.module,
            order=1,
        )

    def test_create_lesson_content(self):
        text_content = TextContent.objects.create(text="Sample text")
        lesson_content = LessonContent.objects.create(
            lesson=self.lesson, content_object=text_content
        )
        self.assertEqual(lesson_content.lesson, self.lesson)
        self.assertEqual(lesson_content.content_object, text_content)


class TextContentModelTest(TestCase):
    def test_create_text_content(self):
        text_content = TextContent.objects.create(text="Sample text content")
        self.assertEqual(text_content.text, "Sample text content")


class FileContentModelTest(TestCase):
    def test_create_file_content(self):
        file_content = FileContent.objects.create(
            file="lesson_files/2023/10/01/sample.txt"
        )
        self.assertEqual(str(file_content.file), "lesson_files/2023/10/01/sample.txt")


class LinkContentModelTest(TestCase):
    def test_create_link_content(self):
        link_content = LinkContent.objects.create(url="https://example.com")
        self.assertEqual(link_content.url, "https://example.com")


class ImageContentModelTest(TestCase):
    def test_create_image_content(self):
        image_content = ImageContent.objects.create(
            image="lesson_images/2023/10/01/sample.jpg"
        )
        self.assertEqual(
            str(image_content.image), "lesson_images/2023/10/01/sample.jpg"
        )


class TestModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )

    def test_create_test(self):
        test = Test.objects.create(
            title="Test Title",
            description="Test Description",
            passing_score=50,
            module=self.module,
        )
        self.assertEqual(test.title, "Test Title")
        self.assertEqual(test.passing_score, 50)


class QuestionsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )
        self.test = Test.objects.create(
            title="Test Title", description="Description", module=self.module
        )

    def test_create_question(self):
        question = Questions.objects.create(
            question="What is 2+2?", order=1, test=self.test
        )
        self.assertEqual(question.question, "What is 2+2?")
        self.assertEqual(question.order, 1)


class AnswersModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )
        self.test = Test.objects.create(
            title="Test Title", description="Description", module=self.module
        )
        self.question = Questions.objects.create(
            question="What is 2+2?", order=1, test=self.test
        )

    def test_create_answer(self):
        answer = Answers.objects.create(answer="4", flag=True, question=self.question)
        self.assertEqual(answer.answer, "4")
        self.assertTrue(answer.flag)


class TaskModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="Description"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Description", category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", description="Description", course=self.course
        )

    def test_create_task(self):
        future_deadline = timezone.now() + timezone.timedelta(days=1)
        task = Task.objects.create(
            title="Test Task",
            description="Task Description",
            deadline=future_deadline,
            module=self.module,
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.deadline, future_deadline)

    def test_deadline_in_past(self):
        past_deadline = timezone.now() - timezone.timedelta(days=1)
        task = Task(
            title="Invalid Task",
            description="Description",
            deadline=past_deadline,
            module=self.module,
        )
        with self.assertRaises(ValidationError):
            task.clean()
