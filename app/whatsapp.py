import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM")  # ej: +14155238886
TO_NUMBER = os.getenv("CALLMEBOT_PHONE")  # tu número destino, ya lo tenés cargado


def enviar_mensaje(texto: str) -> dict:
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_=f"whatsapp:{FROM_NUMBER}",
            to=f"whatsapp:{TO_NUMBER}",
            body=texto
        )
        print(f"📤 Twilio SID: {message.sid}")
        return {"estado": "enviado", "sid": message.sid}
    except Exception as e:
        print(f"❌ Twilio error: {e}")
        return {"estado": "error", "mensaje": str(e)}