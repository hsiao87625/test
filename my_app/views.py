import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.
BASE_CRAIGSLIST_URL = 'https://taipei.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'data:image/jpeg;base64,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'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
        }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)