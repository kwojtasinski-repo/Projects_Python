import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

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

class QuestionVoteTests(TestCase):
    def test_vote_increments_choice_votes(self):
        question = Question.objects.create(
            question_text="Test question",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        choice = Choice.objects.create(
            question=question,
            choice_text="Choice 1",
            votes=0,
        )

        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": choice.id})

        self.assertRedirects(
            response,
            reverse("polls:results", args=(question.id,))
        )

        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_without_choice(self):
        question = Question.objects.create(
            question_text="Test question",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )

        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            "<strong>You didn't select a choice.</strong>",
            response.content.decode(),
        )

    def test_vote_with_invalid_choice(self):
        question = Question.objects.create(
            question_text="Test question",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )

        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": 999})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid choice.")

    def test_vote_on_future_question_returns_404(self):
        question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=1),
        )

        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": 1})

        self.assertEqual(response.status_code, 404)

class NotFoundViewTests(TestCase):
    def test_custom_404_template_used(self):
        response = self.client.get("/definitely-not-existing/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "polls/not_found.html")
