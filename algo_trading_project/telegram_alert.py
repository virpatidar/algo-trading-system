import requests

def send_alert(message, token, chat_id):
    url = f"https://api.telegram.org/bot7593052286:AAF6yIOu4h5gqdK7aEZzX_G4EPxH01o5EQw/sendMessage"
    data = {"chat_id": 6196340861, "text": message}
    
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("❌ Telegram API error:", response.text)
    except Exception as e:
        print("❌ Failed to send alert:", e)