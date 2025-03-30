from flask import Flask, request
import requests

TOKEN = "7347658420:AAFJel5v5zRqa-wF5IrK_lQoI1YPyHOZG0w"
ADMIN_ID = "5634946920"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        username = update["message"]["chat"].get("username", f"User {chat_id}")
        text = update["message"].get("text", "📩 Non-text message received")
        
        # Forward text message
        forward_message(chat_id, text)
        
        # Handle media files
        if "photo" in update["message"]:
            file_id = update["message"]["photo"][-1]["file_id"]
            forward_file(chat_id, file_id, "photo")
        
        if "document" in update["message"]:
            file_id = update["message"]["document"]["file_id"]
            forward_file(chat_id, file_id, "document")
        
        if "video" in update["message"]:
            file_id = update["message"]["video"]["file_id"]
            forward_file(chat_id, file_id, "video")
    
    return "OK"

def forward_message(user_id, text):
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": ADMIN_ID,
        "text": f"User {user_id} sent: {text}"
    })

def forward_file(user_id, file_id, file_type):
    api_endpoint = "sendDocument"
    if file_type == "photo":
        api_endpoint = "sendPhoto"
    elif file_type == "video":
        api_endpoint = "sendVideo"
    
    requests.post(f"{API_URL}/{api_endpoint}", json={
        "chat_id": ADMIN_ID,
        file_type: file_id,
        "caption": f"Forwarded from User {user_id}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
