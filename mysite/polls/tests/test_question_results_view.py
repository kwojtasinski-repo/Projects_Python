import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models import Question

class QuestionResultsViewTests(TestCase):
    def test_results_view_with_past_question(self):
        question = Question.objects.create(
            question_text="Past question.",
            pub_date=timezone.now() - datetime.timedelta(days=5),
        )
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_results_view_with_future_question(self):
        question = Question.objects.create(
            question_text="Future question.",
            pub_date=timezone.now() + datetime.timedelta(days=5),
        )
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
