import pandas as pd

# STEP 1: Load data
df = pd.read_csv(r"finaldaa.csv")

# STEP 2: Fix date + sorting
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by=['Ticker', 'Date'])

# STEP 3: Bollinger Bands
df['MA_20'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=20).mean())

df['STD_20'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=20).std())

df['Upper_Band'] = df['MA_20'] + (2 * df['STD_20'])
df['Lower_Band'] = df['MA_20'] - (2 * df['STD_20'])

print(df[['Ticker', 'Close', 'Upper_Band', 'Lower_Band']].head(25))