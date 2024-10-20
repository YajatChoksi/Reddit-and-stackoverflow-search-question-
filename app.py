from flask import Flask, render_template, request
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Fetch data from Stack Overflow API
def fetch_stackoverflow(query):
    stackoverflow_url = 'https://api.stackexchange.com/2.3/search/advanced'
    params = {
        'order': 'desc',
        'sort': 'relevance',
        'q': query,
        'site': 'stackoverflow',
        
    }

    response = requests.get(stackoverflow_url, params=params)
    if response.status_code == 200:
        return response.json()['items']
    return []

# Fetch data from Reddit API with sorting
def fetch_reddit(query, sort='relevance'):
    headers = {'User-Agent': 'Mozilla/5.0'}
    reddit_url = f'https://www.reddit.com/search.json?q={query}&sort={sort}'
    response = requests.get(reddit_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['children']
    return []

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        sort = request.form['sort']  # Capture the sorting preference for Reddit
        # Fetching results from both platforms
        stackoverflow_results = fetch_stackoverflow(query)
        reddit_results = fetch_reddit(query, sort)
        return render_template('index.html', query=query, stackoverflow=stackoverflow_results, reddit=reddit_results)
    return render_template('index.html')


cache = {}

def cache_results(query, stackoverflow_results, reddit_results):
    cache[query] = {'stackoverflow': stackoverflow_results, 'reddit': reddit_results}

def get_cached_results(query):
    return cache.get(query, None)

if __name__ == '__main__':
    app.run(debug=True)
