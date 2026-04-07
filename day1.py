import yfinance as yf
import pandas as pd

stocks = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "HINDUNILVR.NS"]

all_data = []

for stock in stocks:
    df = yf.download(stock, period="2y", group_by='column')  # IMPORTANT FIX

    df.reset_index(inplace=True)

    # Remove multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df['Ticker'] = stock

    all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)

print(final_df.head())

import sqlite3

conn = sqlite3.connect("stock_data.db")

final_df.to_sql("stock_data", conn, if_exists="replace", index=False)

conn.close()

print("Data stored successfully in SQLite!")