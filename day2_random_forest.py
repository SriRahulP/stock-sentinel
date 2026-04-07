import pandas as pd

# STEP 1: Load data
df = pd.read_csv("finaldaa.csv")

# STEP 2: Fix date + sorting
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by=['Ticker', 'Date'])


# STEP 3: RSI
def calculate_rsi(data, window=14):
    delta = data.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


df['RSI'] = df.groupby('Ticker')['Close'].transform(lambda x: calculate_rsi(x))

# STEP 4: Bollinger Bands
df['MA_20'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=20).mean())
df['STD_20'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=20).std())

df['Upper_Band'] = df['MA_20'] + (2 * df['STD_20'])
df['Lower_Band'] = df['MA_20'] - (2 * df['STD_20'])

# STEP 5: Target
df['Target'] = df.groupby('Ticker')['Close'].shift(-1) > df['Close']
df['Target'] = df['Target'].astype(int)

# STEP 6: Features (NO Volume)
df['BB_Position'] = (df['Close'] - df['Lower_Band']) / (df['Upper_Band'] - df['Lower_Band'])

# STEP 7: Prepare ML data
features = ['RSI', 'MA_7', 'MA_21', 'BB_Position']

df_ml = df.dropna()

X = df_ml[features]
y = df_ml['Target']

# STEP 8: Train/Test split (time-based)
split = int(len(df_ml) * 0.7)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

# STEP 9: Train model
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# STEP 10: Predictions
y_pred = model.predict(X_test)

# STEP 11: Evaluation
from sklearn.metrics import accuracy_score

print("Accuracy:", accuracy_score(y_test, y_pred))

# STEP 12: Generate signals

df_ml['Prediction'] = model.predict(X)

df_ml['Signal'] = df_ml['Prediction'].map({1: 'BUY', 0: 'SELL'})

print(df_ml[['Date', 'Ticker', 'Close', 'Signal']].tail(20))



df_ml.to_csv("final_stock_data.csv", index=False)