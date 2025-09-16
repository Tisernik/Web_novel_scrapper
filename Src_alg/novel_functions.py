# Стандартная команда на запуск
#
#
#


import requests
from bs4 import BeautifulSoup
import random
import time

# List of user agents to bypass bot detection
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
]

def get_html(url):
    headers = {'User-Agent': random.choice(user_agents)}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def save_html(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def main(url):
    #url = 'https://freewebnovel.com/novel/star-odyssey/chapter-3401'  # Replace with the target URL
    #url = 'https://freewebnovel.com/novel/swallowed-star/chapter-1353'
    html_content = get_html(url)
    if html_content:
        save_html(html_content, 'page.html')
        print("HTML content saved successfully.")
    else:
        print("Failed to retrieve HTML content.")

def fetch_and_save_html(url, filename):
    html_content = get_html(url)
    if html_content:
        save_html(html_content, filename)
        print("HTML content saved successfully.")
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    url = 'https://freewebnovel.com/novel/swallowed-star/chapter-1353'
    main(url)
    