from django.test import TestCase

class NotFoundViewTests(TestCase):
    def test_custom_404_template_used(self):
        response = self.client.get("/definitely-not-existing/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "polls/not_found.html")
