import streamlit as st
from src.pipeline import save_price
from src.queries import get_latest_prices

st.title("Crypto API Dashboard")

symbol = st.selectbox("Select coin", ["bitcoin", "ethereum"])
currency = st.selectbox("Select currency", ["usd", "eur"])

if st.button("Fetch Latest Price"):
    try:
        result = save_price(symbol, currency)
        st.success(f"Saved {result['symbol']} price: {result['price']} {result['currency']}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.subheader("Latest Stored Prices")

df = get_latest_prices()
filter_symbol = st.selectbox(
    "Filter table by coin",
    ["all"] + list(df["symbol"].unique())
)

if filter_symbol != "all":
    df = df[df["symbol"] == filter_symbol]
latest_row = df.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("Latest Symbol", latest_row["symbol"])
col2.metric("Latest Price", latest_row["price"])
col3.metric("Currency", latest_row["currency"])
st.dataframe(df)
st.subheader("Statistics")

st.write("Average Price:", round(df["price"].mean(),2))
st.write("Highest Price:", df["price"].max())
st.write("Lowest Price:", df["price"].min())
chart_df = df.sort_values("created_at")

st.subheader("Price Trend")

st.line_chart(
    chart_df,
    x="created_at",
    y="price",
    color="symbol"
)