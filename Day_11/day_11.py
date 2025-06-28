import requests

response = requests.get("https://news.ycombinator.com/news")

print(response.text)