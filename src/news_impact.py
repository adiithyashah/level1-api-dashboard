from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_news_impact(title):

    prompt = f"""
    Analyze this Bitcoin news:

    {title}

    Return only:

    Impact: Bullish/Bearish/Neutral

    Reason: one short sentence
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