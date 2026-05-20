def calculate_stats(df):

    avg_price = round(df["price"].mean(),2)

    max_price = df["price"].max()

    min_price = df["price"].min()

    volatility = round(df["price"].std(),2)

    return {
        "average": avg_price,
        "highest": max_price,
        "lowest": min_price,
        "volatility": volatility
    }