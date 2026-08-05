import os
requests = __import__('requests')
from dotenv import load_dotenv

load_dotenv()

class TelegramService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, text: str):
        if not self.token or not self.chat_id:
            print("⚠️ [Telegram] Token ou Chat ID não configurados no .env")
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("📱 [Telegram] Mensagem enviada com sucesso!")
                return True
            else:
                print(f"❌ [Telegram] Erro ao enviar mensagem: {response.text}")
                return False
        except Exception as e:
            print(f"❌ [Telegram] Erro de conexão: {e}")
            return False