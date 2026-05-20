# Crypto API Dashboard

An end-to-end data pipeline that fetches live cryptocurrency prices from an external API, stores the data in PostgreSQL, and displays insights through an interactive Streamlit dashboard.

## Features

- External API integration using Python
- PostgreSQL data storage
- Streamlit dashboard
- Price trend visualization
- Summary metrics
- Coin filtering
- Auto-refresh
- CSV export
- Git/GitHub version control

## Tech Stack

- Python
- PostgreSQL
- Streamlit
- Pandas
- Requests
- psycopg2
- python-dotenv

## System Flow

API → Python → PostgreSQL → Streamlit Dashboard

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py