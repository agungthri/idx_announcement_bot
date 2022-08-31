import requests

# telegram bot to send messege 
def send_message(msg):
    token = "your Telegram API token"
    chatID = "your chat ID (group or private)"
    params = {"chat_id":chatID,"text":msg}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.get(url, params=params, timeout=30)
