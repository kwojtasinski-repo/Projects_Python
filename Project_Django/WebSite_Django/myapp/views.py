import json
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .decorators import post_only_redirect_home
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')

@post_only_redirect_home
def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    final_postings = __getPosts(data)

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'myapp/new_search.html', stuff_for_frontend)

def __getPostsFromHtml(data):
    print("Using HTML parsing")
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'cl-static-search-result'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='title').text
        post_url = post.find('a').get('href')

        post_price = post.find(class_='price').text if post.find(class_='price') else 'N/A'

        if post.find(class_='result-image'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append({
            "title": post_title,
            "url": post_url,
            "price": post_price,
            "image": post_image_url
        })

    return final_postings


def __getPostsFromJson(data):
    print("Using JSON parsing")
    soup = BeautifulSoup(data, features='html.parser')
    script = soup.find('script', type='application/ld+json', id='ld_searchpage_results')

    if not script:
        return []

    json_data = json.loads(script.string or "{}")
    if json_data.get('@type') != 'ItemList' or 'itemListElement' not in json_data:
        return []

    final_postings = []

    for post in json_data['itemListElement']:
        item = post.get('item', {})

        post_title = item.get('name', 'No Title')
        post_url = item.get('url', '#')
        post_price = item.get('offers', {}).get('price', 'N/A')

        images = item.get('image') or []
        post_image_url = images[0] if isinstance(images, list) and images else 'https://craigslist.org/images/peace.jpg'

        final_postings.append({
            "title": post_title,
            "url": post_url,
            "price": post_price,
            "image": post_image_url
        })

    return final_postings

def __getPosts(data):
    html_posts = __getPostsFromHtml(data)
    json_posts = __getPostsFromJson(data)

    html_by_title = {p["title"]: p for p in html_posts}

    final = []

    for post in json_posts:
        title = post["title"]

        if title in html_by_title:
            post["url"] = html_by_title[title]["url"]

        final.append(post)

    return final