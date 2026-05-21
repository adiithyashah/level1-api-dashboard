import os
from groq import Groq
from dotenv import load_dotenv
from src.news import get_market_news
from src.sentiment import calculate_sentiment

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_market_insight(stats, symbol):

    news = get_market_news(symbol)
    sentiment = calculate_sentiment(news)

    prompt = f"""
    You are a professional market analyst.

    Analyze the market using both price data and news.

    Symbol: {symbol}

    Price Analytics:
    Average Price: {stats["average"]}
    Highest Price: {stats["highest"]}
    Lowest Price: {stats["lowest"]}
    Volatility: {stats["volatility"]}

    Market News:
    {news}

    Give:
    - Market trend
    - News Sentiment: {sentiment}
    - News impact
    - Volatility observation
    - Short conclusion

    Keep it concise.
    Do not give financial advice.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
