import os
import requests
from dotenv import load_dotenv

load_dotenv()


def is_bitcoin_relevant(title):

    title_lower = title.lower()

    bitcoin_keywords = [
        "bitcoin",
        "btc"
    ]

    reject_keywords = [
        "ethereum",
        "eth",
        "solana",
        "xrp",
        "dogecoin",
        "cardano",
        "bnb",
        "shiba"
    ]

    has_bitcoin_keyword = any(
        keyword in title_lower for keyword in bitcoin_keywords
    )

    has_rejected_keyword = any(
        keyword in title_lower for keyword in reject_keywords
    )

    if has_bitcoin_keyword and not has_rejected_keyword:
        return True

    return False


def get_market_news(symbol):

    api_key = os.getenv("NEWS_API_KEY")

    query = "bitcoin OR btc"

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": api_key
    }

    response = requests.get(
        url,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    articles = data.get(
        "articles",
        []
    )

    news_data = []

    for article in articles:

        title = article.get(
            "title",
            "No title"
        )

        source = article.get(
            "source",
            {}
        ).get(
            "name",
            "Unknown"
        )

        if is_bitcoin_relevant(title):

            news_data.append(
                {
                    "title": title,
                    "source": source
                }
            )

        if len(news_data) == 5:
            break

    if not news_data:
        return [
            {
                "title": "No Bitcoin-specific news found at the moment.",
                "source": "System"
            }
        ]

    return news_data