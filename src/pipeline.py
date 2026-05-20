from src.api_client import fetch_crypto_price
from src.database import get_connection

def save_price(symbol="bitcoin", currency="usd"):

    data = fetch_crypto_price(symbol, currency)

    print("Fetched:", data)

    conn = get_connection()
    print("Connected to database")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO api_prices(symbol,price,currency)
        VALUES(%s,%s,%s)
        """,
        (
            data["symbol"],
            data["price"],
            data["currency"]
        )
    )

    conn.commit()

    print("Data inserted")

    cursor.close()
    conn.close()

    return data