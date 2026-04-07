import pandas as pd

df = pd.read_csv("finaldaa.csv")

print(df.head())
print(df.columns)


df['Date'] = pd.to_datetime(df['Date'])

df = df.sort_values(by=['Ticker', 'Date'])


def calculate_rsi(data, window=14):
    delta = data.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


df['RSI'] = df.groupby('Ticker')['Close'].transform(lambda x: calculate_rsi(x))

print(df[['Ticker', 'Close', 'RSI']].head(20))