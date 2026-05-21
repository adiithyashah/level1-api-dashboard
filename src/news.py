import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_market_news(symbol):

    api_key = os.getenv("NEWS_API_KEY")

    if symbol == "bitcoin":
        query = "bitcoin cryptocurrency"

    elif symbol == "ethereum":
        query = "ethereum cryptocurrency"

    else:
        query = "cryptocurrency market"

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    articles = data.get("articles", [])

    news_titles = []

    for article in articles:
        title = article.get("title")

        if title:
            news_titles.append(title)

    if not news_titles:
        return ["No recent news found"]

    return news_titles