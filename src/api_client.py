import requests

def fetch_crypto_price(symbol="bitcoin", currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": symbol,
        "vs_currencies": currency
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    print("API response:", data)

    if symbol not in data:
        raise ValueError(f"Symbol '{symbol}' not found in API response")

    if currency not in data[symbol]:
        raise ValueError(f"Currency '{currency}' not found for {symbol}")

    return {
        "symbol": symbol,
        "price": data[symbol][currency],
        "currency": currency
    }