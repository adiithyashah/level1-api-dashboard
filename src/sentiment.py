def calculate_sentiment(news):

    positive_words = [
        "growth",
        "increasing",
        "interest",
        "improvements",
        "higher",
        "rises",
        "surge",
        "bullish"
    ]

    negative_words = [
        "decline",
        "drop",
        "loss",
        "risk",
        "fall",
        "crash",
        "bearish"
    ]

    score = 0

    for article in news:

        title = article.get("title", "")

        text = title.lower()

        for word in positive_words:
            if word in text:
                score += 1

        for word in negative_words:
            if word in text:
                score -= 1

    if score > 0:
        return "Positive"

    elif score < 0:
        return "Negative"

    return "Neutral"