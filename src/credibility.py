def check_news_credibility(source_name):

    trusted_sources = [
        "Reuters",
        "Bloomberg",
        "CNBC",
        "CoinDesk",
        "The Block",
        "Wall Street Journal",
        "Financial Times",
        "MarketWatch",
        "Forbes"
    ]

    if source_name in trusted_sources:
        return "High"

    return "Medium"