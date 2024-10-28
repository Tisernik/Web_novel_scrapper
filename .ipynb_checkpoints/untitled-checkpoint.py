from random import seed
import requests

url = "https://freewebnovel.com/lord-of-the-mysteries.html"
session_obj = requests.Session()
response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})

print(response.content)
