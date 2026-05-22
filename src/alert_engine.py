def generate_bitcoin_alerts(stats, sentiment, news):

    alerts = []

    volatility = stats["volatility"]

    if volatility > 500:
        alerts.append(
            {
                "level": "High",
                "message": "High volatility detected. Bitcoin price movement is unstable compared to recent observations."
            }
        )

    if sentiment == "Negative":
        alerts.append(
            {
                "level": "High",
                "message": "Negative news sentiment detected. Monitor for possible downside pressure or risk-off behavior."
            }
        )

    elif sentiment == "Positive":
        alerts.append(
            {
                "level": "Medium",
                "message": "Positive news sentiment detected. Market attention may be increasing around Bitcoin."
            }
        )

    important_keywords = [
        "ETF",
        "SEC",
        "Federal Reserve",
        "Fed",
        "inflation",
        "hack",
        "ban",
        "lawsuit",
        "approval",
        "liquidation",
        "whale"
    ]

    detected_keywords = set()

    for article in news:
        title = article.get("title", "")

        for keyword in important_keywords:
            if keyword.lower() in title.lower():
                detected_keywords.add(keyword)

    for keyword in detected_keywords:
        alerts.append(
            {
                "level": "Medium",
                "message": f"Important market keyword detected: {keyword}."
            }
        )

    if not alerts:
        alerts.append(
            {
                "level": "Low",
                "message": "No major alert detected from current price analytics and news."
            }
        )

    return alerts