from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Todo


class TodoAppTests(TestCase):

    def test_home_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_todo_post(self):
        response = self.client.post(
            reverse("add_todo"),
            {"content": "Test item"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)

    def test_add_todo_get_redirect(self):
        response = self.client.get(reverse("add_todo"))
        self.assertEqual(response.status_code, 302)

    def test_delete_existing_todo(self):
        todo = Todo.objects.create(
            content="To delete",
            add_date=timezone.now()
        )

        response = self.client.post(
            reverse("delete_todo", args=[todo.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_non_existing_todo(self):
        response = self.client.post(
            reverse("delete_todo", args=[999])
        )

        self.assertEqual(response.status_code, 302)
