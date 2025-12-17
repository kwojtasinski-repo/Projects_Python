import json
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus

BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/?query={}"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"
DEFAULT_IMAGE_URL = "https://craigslist.org/images/peace.jpg"


def fetch_posts(search: str) -> list[dict]:
    """
    Main entry point for scraping Craigslist.
    Returns a list of normalized post dictionaries.
    """
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    response = requests.get(final_url, timeout=10)
    response.raise_for_status()

    html = response.text

    html_posts = _get_posts_from_html(html)
    json_posts = _get_posts_from_json(html)

    return _merge_posts(html_posts, json_posts)


# ------------------------
# Internal helpers
# ------------------------

def _get_posts_from_html(html: str) -> list[dict]:
    soup = BeautifulSoup(html, features="html.parser")
    post_listings = soup.find_all("li", {"class": "cl-static-search-result"})

    posts = []

    for post in post_listings:
        title_tag = post.find(class_="title")
        if not title_tag:
            continue

        title = title_tag.text.strip()
        url = post.find("a").get("href")

        price_tag = post.find(class_="price")
        price = price_tag.text.strip() if price_tag else "N/A"

        image_tag = post.find(class_="result-image")
        if image_tag and image_tag.get("data-ids"):
            image_id = image_tag.get("data-ids").split(",")[0].split(":")[1]
            image_url = BASE_IMAGE_URL.format(image_id)
        else:
            image_url = DEFAULT_IMAGE_URL

        posts.append({
            "title": title,
            "url": url,
            "price": price,
            "image": image_url,
        })

    return posts


def _get_posts_from_json(html: str) -> list[dict]:
    soup = BeautifulSoup(html, features="html.parser")
    script = soup.find(
        "script",
        type="application/ld+json",
        id="ld_searchpage_results",
    )

    if not script or not script.string:
        return []

    try:
        json_data = json.loads(script.string)
    except json.JSONDecodeError:
        return []

    if json_data.get("@type") != "ItemList":
        return []

    posts = []

    for post in json_data.get("itemListElement", []):
        item = post.get("item", {})

        title = item.get("name", "No Title")
        url = item.get("url", "#")
        price = item.get("offers", {}).get("price", "N/A")

        images = item.get("image") or []
        image_url = images[0] if isinstance(images, list) and images else DEFAULT_IMAGE_URL

        posts.append({
            "title": title,
            "url": url,
            "price": price,
            "image": image_url,
        })

    return posts


def _merge_posts(html_posts: list[dict], json_posts: list[dict]) -> list[dict]:
    html_by_title = {post["title"]: post for post in html_posts}

    final = []

    for post in json_posts:
        title = post["title"]
        if title in html_by_title:
            post["url"] = html_by_title[title]["url"]

        final.append(post)

    return final
