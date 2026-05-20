import requests

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin",
    "vs_currencies": "usd"
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)

data = response.json()

print("Full Response:", data)

print("Bitcoin Price:", data["bitcoin"]["usd"])