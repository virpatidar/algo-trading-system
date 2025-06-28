import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    data.dropna(inplace=True)
    return data
