from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_market_question(question, stats, symbol):

    prompt = f"""
    Market Data:

    Symbol: {symbol}
    Average Price: {stats["average"]}
    Highest Price: {stats["highest"]}
    Lowest Price: {stats["lowest"]}
    Volatility: {stats["volatility"]}

    User Question:

    {question}

    Answer professionally and briefly.
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