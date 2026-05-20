import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_market_insight(stats, symbol):

    prompt = f"""
    You are a professional market analyst.

    Analyze:

    Symbol: {symbol}
    Average Price: {stats["average"]}
    Highest Price: {stats["highest"]}
    Lowest Price: {stats["lowest"]}
    Volatility: {stats["volatility"]}

    Give:
    - Market trend
    - Volatility observation
    - Short insight

    Keep it concise.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content