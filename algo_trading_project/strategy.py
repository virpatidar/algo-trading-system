import pandas as pd

def calculate_indicators(df):
    df['20_MA'] = df['Close'].rolling(window=20).mean()
    df['50_MA'] = df['Close'].rolling(window=50).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def generate_signals(df):
    signals = []
    for i in range(1, len(df)):
        if df['RSI'].iloc[i] < 30 and df['20_MA'].iloc[i] > df['50_MA'].iloc[i]:
            signals.append("BUY")
        else:
            signals.append("")
    signals.insert(0, "")
    df["Signal"] = signals
    return df
