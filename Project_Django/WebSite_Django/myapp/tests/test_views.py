from django.test import TestCase
from django.urls import reverse
from  ..models import Search
from unittest.mock import patch

HTML_RESPONSE = """
<html>
<li class="cl-static-search-result">
  <a href="https://example.com">
    <span class="title">Test Item</span>
    <span class="price">$123</span>
  </a>
</li>

<script type="application/ld+json" id="ld_searchpage_results">
{
  "@type": "ItemList",
  "itemListElement": [
    {
      "item": {
        "name": "Test Item",
        "url": "https://json-url.com",
        "offers": { "price": "$999" },
        "image": ["https://example.com/image.jpg"]
      }
    }
  ]
}
</script>
</html>
"""

class HomeViewTest(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")

class NewSearchViewTest(TestCase):
    def test_post_creates_search_and_renders_results(self):
        response = self.client.post(
            reverse("new_search"),
            data={"search": "laptop"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/new_search.html")
        self.assertEqual(Search.objects.count(), 1)
        self.assertEqual(Search.objects.first().search, "laptop")

    @patch("myapp.scraper.requests.get")
    def test_new_search_fetches_and_renders_posts(self, mock_get):
        # mock HTTP response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = HTML_RESPONSE

        response = self.client.post(
            reverse("new_search"),
            data={"search": "test item"},
        )

        # HTTP
        self.assertEqual(response.status_code, 200)

        # DB
        self.assertEqual(Search.objects.count(), 1)
        self.assertEqual(Search.objects.first().search, "test item")

        # Template context
        self.assertIn("final_postings", response.context)
        posts = response.context["final_postings"]

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["title"], "Test Item")

        # URL preference (HTML over JSON)
        self.assertEqual(posts[0]["url"], "https://example.com")
