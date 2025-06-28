from data_fetcher import fetch_stock_data
from strategy import calculate_indicators, generate_signals
from ml_model import prepare_features, train_model
from sheet_logger import connect_to_sheet, log_data
from telegram_alert import send_alert

def run_pipeline():
    stock_list = ["RELIANCE.NS", "INFY.NS", "TCS.NS"]
    all_signals = []

    for stock in stock_list:
        df = fetch_stock_data(stock)
        df = calculate_indicators(df)
        df = generate_signals(df)
        all_signals.append(df)

    sheet = connect_to_sheet("Algo_Trading_Log")
    for i, df in enumerate(all_signals):
        log_data(sheet, df, stock_list[i].replace(".NS", ""))
        if "BUY" in df["Signal"].values:
            send_alert(f"Buy signal triggered for {stock_list[i]}", "7593052286:AAF6yIOu4h5gqdK7aEZzX_G4EPxH01o5EQw", "6196340861")

    # ML Model
    X_train, X_test, y_train, y_test = prepare_features(all_signals[0])
    model, acc = train_model(X_train, X_test, y_train, y_test)
    print(f"Prediction Accuracy: {acc:.2f}")

TELEGRAM_TOKEN = "7593052286:AAF6yIOu4h5gqdK7aEZzX_G4EPxH01o5EQw"  # Replace with your real token
CHAT_ID = "6196340861"  # Replace with your real chat ID

send_alert("📢 BUY signal for RELIANCE!", TELEGRAM_TOKEN, CHAT_ID)

if __name__ == "__main__":
    run_pipeline()
