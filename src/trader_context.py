import os
from groq import Groq
from dotenv import load_dotenv
from src.credibility import check_news_credibility

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_trader_context(stats, sentiment, news):

    news_context = []

    for article in news:
        title = article.get("title", "")
        source = article.get("source", "Unknown")
        credibility = check_news_credibility(source)

        news_context.append(
            f"- {title} | Source: {source} | Credibility: {credibility}"
        )

    prompt = f"""
    You are a Bitcoin market intelligence analyst.

    Analyze the current Bitcoin situation for a trader or investor.

    Price Analytics:
    Average Price: {stats["average"]}
    Highest Price: {stats["highest"]}
    Lowest Price: {stats["lowest"]}
    Volatility: {stats["volatility"]}

    News Sentiment:
    {sentiment}

    Recent News:
    {news_context}

    Return the response in this exact format:

    Current Market Condition:
    ...

    Key News Catalysts:
    ...

    Trader Watchpoints:
    ...

    Risk Notes:
    ...

    Keep it concise.
    Do not give buy or sell advice.
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