import pandas as pd
from src.database import get_connection

def get_latest_prices():
    conn = get_connection()

    query = """
    SELECT symbol, price, currency, created_at
    FROM api_prices
    ORDER BY created_at DESC
    LIMIT 20;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    df = df.reset_index(drop=True)

    return df