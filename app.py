import streamlit as st

from src.pipeline import save_price
from src.queries import get_latest_prices
from src.analytics import calculate_stats
from src.ai_insights import generate_market_insight
from src.market_chat import ask_market_question
from src.news import get_market_news
from src.sentiment import calculate_sentiment
from src.credibility import check_news_credibility
from src.news_impact import analyze_news_impact
from src.trader_context import generate_trader_context
from src.alert_engine import generate_bitcoin_alerts
from src.focus_panel import build_focus_panel

@st.cache_data(ttl=300)
def cached_market_news(symbol):
    return get_market_news(symbol)


@st.cache_data(ttl=300)
def cached_market_insight(symbol, average, highest, lowest, volatility):
    stats = {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "volatility": volatility
    }

    return generate_market_insight(stats, symbol)


@st.cache_data(ttl=600)
def cached_news_impact(title):
    return analyze_news_impact(title)


@st.cache_data(ttl=300)
def cached_trader_context(average, highest, lowest, volatility, sentiment, news):

    stats = {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "volatility": volatility
    }

    return generate_trader_context(
        stats,
        sentiment,
        news
    )


st.title("Bitcoin Intelligence Terminal")

if st.button("Refresh Intelligence"):
    st.cache_data.clear()
    st.rerun()


# -------------------------
# User Inputs
# -------------------------

symbol = "bitcoin"

st.caption("Focused real-time intelligence system for Bitcoin market analysis.")

currency = st.selectbox(
    "Select Currency",
    ["usd", "eur"]
)


# -------------------------
# Fetch Latest Price
# -------------------------

if st.button("Fetch Latest Price"):

    try:
        result = save_price(symbol, currency)

        st.success(
            f"Saved {result['symbol']} price: {result['price']} {result['currency']}"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")


# -------------------------
# Read Data From Database
# -------------------------

df = get_latest_prices()


# -------------------------
# Filter Data
# -------------------------

filter_symbol = "bitcoin"
df = df[df["symbol"] == filter_symbol]


# -------------------------
# Calculate Analytics
# -------------------------

stats = calculate_stats(df)

news = cached_market_news(filter_symbol)

sentiment = calculate_sentiment(news)

alerts = generate_bitcoin_alerts(
    stats,
    sentiment,
    news
)

focus = build_focus_panel(
    stats,
    sentiment,
    alerts
)


# -------------------------
# Bitcoin Alerts
# -------------------------
st.subheader("Bitcoin Alerts")

for alert in alerts:

    level = alert["level"]
    message = alert["message"]

    if level == "High":
        st.error(f"{level}: {message}")

    elif level == "Medium":
        st.warning(f"{level}: {message}")

    else:
        st.info(f"{level}: {message}")


# -------------------------
# Bitcoin Focus Panel
# -------------------------

st.subheader("Bitcoin Focus Panel")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Bias", focus["market_bias"])
col2.metric("News Sentiment", focus["sentiment"])
col3.metric("Volatility", focus["volatility_state"])
col4.metric("Critical Alerts", focus["critical_alerts"])

with st.expander("View technical analytics"):
    st.write("Average Price:", stats["average"])
    st.write("Highest Price:", stats["highest"])
    st.write("Lowest Price:", stats["lowest"])
    st.write("Volatility:", stats["volatility"])
    st.write("Volatility %:", f"{focus['volatility_percent']}%")


# -------------------------
# Market News Section
# -------------------------

st.subheader("Market News + Impact")

for article in news:

    title = article["title"]
    source = article["source"]
    credibility = check_news_credibility(source)
    impact = cached_news_impact(title)

    st.write(f"• {title}")
    st.caption(f"Source: {source} | Credibility: {credibility}")
    st.info(impact)


# -------------------------
# AI Market Insight
# -------------------------

insight = cached_market_insight(
    filter_symbol,
    stats["average"],
    stats["highest"],
    stats["lowest"],
    stats["volatility"]
)

st.subheader("AI Market Insight")
st.info(insight)
trader_context = cached_trader_context(
    stats["average"],
    stats["highest"],
    stats["lowest"],
    stats["volatility"],
    sentiment,
    news
)

st.subheader("Trader Context")
st.warning(trader_context)


# -------------------------
# AI Market Chat
# -------------------------

st.subheader("Ask AI About Market")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Ask a market question")

if st.button("Ask AI"):

    if question:
        answer = ask_market_question(
            question,
            stats,
            filter_symbol
        )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

    else:
        st.warning("Please enter a question first.")

for chat in st.session_state.chat_history:
    st.write("**You:**", chat["question"])
    st.write("**AI:**", chat["answer"])
    st.divider()