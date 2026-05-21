import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.pipeline import save_price
from src.queries import get_latest_prices
from src.analytics import calculate_stats
from src.ai_insights import generate_market_insight
from src.market_chat import ask_market_question
from src.news import get_market_news
from src.sentiment import calculate_sentiment


st.title("AI Market Intelligence Dashboard")

st_autorefresh(
    interval=10000,
    key="refresh"
)


# -------------------------
# User Inputs
# -------------------------

symbol = st.selectbox(
    "Select Coin",
    ["bitcoin", "ethereum"]
)

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

filter_symbol = st.selectbox(
    "Filter table by coin",
    ["all"] + list(df["symbol"].unique())
)

if filter_symbol != "all":
    df = df[df["symbol"] == filter_symbol]


# -------------------------
# Calculate Analytics
# -------------------------

stats = calculate_stats(df)

news = get_market_news(filter_symbol)

sentiment = calculate_sentiment(news)


# -------------------------
# Market Analytics Section
# -------------------------

st.subheader("Market Analytics")

col1, col2 = st.columns(2)

col1.metric("Average Price", stats["average"])
col2.metric("Volatility", stats["volatility"])

col1.metric("Highest Price", stats["highest"])
col2.metric("Lowest Price", stats["lowest"])

st.metric("News Sentiment", sentiment)


# -------------------------
# Market News Section
# -------------------------

st.subheader("Market News")

for article in news:
    st.write("•", article)


# -------------------------
# AI Market Insight
# -------------------------

insight = generate_market_insight(
    stats,
    filter_symbol
)

st.subheader("AI Market Insight")
st.info(insight)


# -------------------------
# Latest Stored Prices
# -------------------------

st.subheader("Latest Stored Prices")

st.dataframe(df)


# -------------------------
# Price Trend Chart
# -------------------------

chart_df = df.sort_values("created_at")

st.subheader("Price Trend")

st.line_chart(
    chart_df,
    x="created_at",
    y="price",
    color="symbol"
)


# -------------------------
# Download CSV
# -------------------------

csv = df.to_csv(index=False)

st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="crypto_prices.csv",
    mime="text/csv"
)


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