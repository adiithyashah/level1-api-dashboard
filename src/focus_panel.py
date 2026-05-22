def build_focus_panel(stats, sentiment, alerts):

    average = stats["average"]
    volatility = stats["volatility"]

    if average > 0:
        volatility_percent = round((volatility / average) * 100, 2)
    else:
        volatility_percent = 0

    if volatility_percent >= 1:
        volatility_state = "High"
    elif volatility_percent >= 0.3:
        volatility_state = "Moderate"
    else:
        volatility_state = "Low"

    critical_alerts = 0

    for alert in alerts:
        if alert["level"] == "High":
            critical_alerts += 1

    if sentiment == "Positive" and volatility_state != "High":
        market_bias = "Constructive"
    elif sentiment == "Negative":
        market_bias = "Cautious"
    elif volatility_state == "High":
        market_bias = "Unstable"
    else:
        market_bias = "Neutral"

    return {
        "market_bias": market_bias,
        "sentiment": sentiment,
        "volatility_state": volatility_state,
        "critical_alerts": critical_alerts,
        "volatility_percent": volatility_percent
    }