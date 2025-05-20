from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from courses.models import Course, Category
from ..models import Module, Test, Questions, Answers


class ConstructViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@gmail.com", password="testpass", is_author=True
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.course = Course.objects.create(
            name="Test Course", author=self.user, category=self.category
        )
        self.module = Module.objects.create(
            name="Test Module", course=self.course, order=1
        )
        self.test = Test.objects.create(title="Test Test", module=self.module, order=1)
        self.question1 = Questions.objects.create(
            question="Question 1", order=1, test=self.test
        )
        self.answer1 = Answers.objects.create(
            answer="Answer 1", flag=True, question=self.question1
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_question_create_view(self):
        url = reverse("construct:add_question", kwargs={"test_id": self.test.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tests/questions/create.html")
        data = {"question": "New Question"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Questions.objects.filter(question="New Question").exists())
        self.assertRedirects(
            response, reverse("construct:test_detail", kwargs={"pk": self.test.id})
        )

    def test_question_detail_view(self):
        url = reverse(
            "construct:question_detail",
            kwargs={"pk": self.question1.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tests/questions/detail.html")
        self.assertEqual(response.context["question"], self.question1)

    def test_question_update_view(self):
        url = reverse("construct:question_edit", kwargs={"pk": self.question1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tests/questions/form.html")
        data = {"question": "Updated Question"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.question1.refresh_from_db()
        self.assertEqual(self.question1.question, "Updated Question")

    def test_question_delete(self):
        question = Questions.objects.create(
            question="Question 2", order=2, test=self.test
        )
        url = reverse(
            "construct:question_delete",
            kwargs={"pk": question.id},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Questions.objects.filter(id=question.id).exists())
        self.assertRedirects(
            response, reverse("construct:test_detail", kwargs={"pk": self.test.id})
        )

    def test_answer_create_view(self):
        url = reverse(
            "construct:answer_create", kwargs={"question_id": self.question1.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tests/answers/create.html")
        data = {"answer": "New Answer", "flag": True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Answers.objects.filter(answer="New Answer").exists())
        self.assertRedirects(
            response,
            reverse(
                "construct:question_detail",
                kwargs={"pk": self.question1.id},
            ),
        )

    def test_answer_update_view(self):
        url = reverse("construct:answer_edit", kwargs={"pk": self.answer1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tests/answers/form.html")
        data = {"answer": "Updated Answer", "flag": False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.answer1.refresh_from_db()
        self.assertEqual(self.answer1.answer, "Updated Answer")

    def test_answer_delete_view(self):
        answer = Answers.objects.create(
            answer="Answer 2", flag=False, question=self.question1
        )
        url = reverse(
            "construct:answer_delete",
            kwargs={"pk": answer.id},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Answers.objects.filter(id=answer.id).exists())
        self.assertRedirects(
            response,
            reverse(
                "construct:question_detail",
                kwargs={"pk": self.question1.id},
            ),
        )
