from django.test import TestCase
from ..models import Search


class SearchModelTest(TestCase):
    def test_search_is_created(self):
        search = Search.objects.create(search="django")

        self.assertEqual(search.search, "django")
        self.assertIsNotNone(search.created)

    def test_plural_name(self):
        self.assertEqual(str(Search._meta.verbose_name_plural), "Searches")
