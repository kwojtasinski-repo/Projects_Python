from  ..scraper import (
    _get_posts_from_html,
    _get_posts_from_json,
    _merge_posts,
    fetch_posts
)
from unittest.mock import patch, Mock
from django.test import TestCase

HTML_FIXTURE = """
<li class="cl-static-search-result">
  <a href="https://example.com">
    <span class="title">Test Item</span>
    <span class="price">$100</span>
  </a>
</li>
"""

JSON_FIXTURE = """
<script type="application/ld+json" id="ld_searchpage_results">
{
  "@type": "ItemList",
  "itemListElement": [
    {
      "item": {
        "name": "Test Item",
        "url": "https://example.com",
        "offers": { "price": "$100" },
        "image": ["https://example.com/image.jpg"]
      }
    }
  ]
}
</script>
"""

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


class ScraperTests(TestCase):
    def test_html_parser_returns_posts(self):
        posts = _get_posts_from_html(HTML_FIXTURE)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["title"], "Test Item")


    def test_json_parser_returns_posts(self):
        posts = _get_posts_from_json(JSON_FIXTURE)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["price"], "$100")


    def test_merge_posts_prefers_html_url(self):
        html = [{"title": "A", "url": "html_url"}]
        json_posts = [{"title": "A", "url": "json_url"}]

        merged = _merge_posts(html, json_posts)

        self.assertEqual(merged[0]["url"], "html_url")

    def test_merge_posts_keeps_json_only_posts(self):
        html = []
        json_posts = [{"title": "Only JSON", "url": "json_url"}]

        merged = _merge_posts(html, json_posts)

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["title"], "Only JSON")

    @patch("myapp.scraper.requests.get")
    def test_fetch_posts_returns_merged_results(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = HTML_RESPONSE
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        # act
        posts = fetch_posts("test item")

        # assert
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post["title"], "Test Item")
        self.assertIn(post["price"], ["$999", "$123"])
        self.assertEqual(post["url"], "https://example.com")  # HTML wins
        self.assertTrue(post["image"].startswith("http"))
