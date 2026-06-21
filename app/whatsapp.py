import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM")
TO_NUMBER = os.getenv("CALLMEBOT_PHONE")


def enviar_mensaje(texto: str) -> dict:
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_=f"whatsapp:{FROM_NUMBER}",
            to=f"whatsapp:{TO_NUMBER}",
            body=texto
        )
        return {"estado": "enviado", "sid": message.sid}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}


def enviar_imagen(imagen_bytes: bytes, caption: str = "") -> dict:
    try:
        # Subís la imagen a Twilio como media
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Guardás temporalmente y enviás como media_url
        # Twilio Sandbox no soporta media upload directo,
        # usamos imgbb gratis para hostear la imagen
        url = subir_imagen_imgbb(imagen_bytes)
        if not url:
            return {"estado": "error", "mensaje": "No se pudo subir la imagen"}

        message = client.messages.create(
            from_=f"whatsapp:{FROM_NUMBER}",
            to=f"whatsapp:{TO_NUMBER}",
            body=caption,
            media_url=[url]
        )
        return {"estado": "enviado", "sid": message.sid}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}


def subir_imagen_imgbb(imagen_bytes: bytes) -> str | None:
    try:
        import base64
        IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
        imagen_b64 = base64.b64encode(imagen_bytes).decode("utf-8")
        respuesta = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": IMGBB_API_KEY, "image": imagen_b64}
        )
        data = respuesta.json()
        return data["data"]["url"]
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        return None


def descargar_media(media_url: str) -> bytes | None:
    try:
        respuesta = requests.get(
            media_url,
            auth=(ACCOUNT_SID, AUTH_TOKEN)
        )
        return respuesta.content
    except Exception as e:
        print(f"❌ Error descargando media: {e}")
        return None