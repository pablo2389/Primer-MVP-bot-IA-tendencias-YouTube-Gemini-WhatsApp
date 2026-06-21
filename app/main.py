import asyncio
import traceback
from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.whatsapp import enviar_mensaje
from app.youtube import buscar_videos
from app.gemini import analizar_tendencias
from app.comandos import procesar_mensaje


app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "Bot IA WhatsApp funcionando 🚀"}


@app.get("/test-whatsapp")
def test_whatsapp():
    resultado = enviar_mensaje("🤖 Bot conectado correctamente desde Python")
    return {"respuesta": resultado}


@app.get("/trending")
def trending(tema: str = "seo"):
    videos = buscar_videos(tema)
    return {"tema": tema, "videos": videos}


@app.get("/ideas")
def ideas(tema: str = "seo"):
    videos = buscar_videos(tema)
    analisis = analizar_tendencias(videos)
    return {"tema": tema, "analisis": analisis}


@app.get("/viral")
def viral(tema: str = "seo"):
    videos = buscar_videos(tema)
    analisis = analizar_tendencias(videos)
    return {"tema": tema, "resultado": analisis}


@app.get("/whatsapp-viral")
def whatsapp_viral(tema: str = "seo"):
    videos = buscar_videos(tema)
    analisis = analizar_tendencias(videos)
    try:
        enviar_mensaje(analisis)
        whatsapp = "enviado correctamente"
    except Exception as e:
        whatsapp = f"error whatsapp: {str(e)}"
    return {"ok": True, "tema": tema, "whatsapp": whatsapp}


@app.get("/descubrir")
def descubrir():
    nichos = [
        "google business", "seo local", "chatgpt",
        "inteligencia artificial", "wordpress", "react",
        "marketing digital", "youtube shorts",
    ]
    resultado = {}
    for nicho in nichos:
        try:
            videos = buscar_videos(nicho, max_results=30)
            resultado[nicho] = videos[:5]
        except Exception as e:
            resultado[nicho] = {"error": str(e)}
    return resultado


@app.get("/oportunidad")
def oportunidad():
    videos = []
    nichos = ["google business", "seo local", "chatgpt",
              "inteligencia artificial", "wordpress", "react"]
    for nicho in nichos:
        try:
            videos.extend(buscar_videos(nicho, max_results=10))
        except Exception as e:
            print(f"Error en {nicho}: {e}")
    videos.sort(key=lambda x: x["score_viral"], reverse=True)
    top = videos[:20]
    analisis = analizar_tendencias(top)
    return {"videos": top, "analisis": analisis}


@app.post("/webhook")


@app.post("/webhook")
async def webhook(Body: str = Form(default=""), From: str = Form(default="")):
    import traceback
    mensaje = Body.strip()
    numero = From.strip()
    print(f"📩 Mensaje de {numero}: {mensaje}")

    try:
        respuesta = procesar_mensaje(mensaje)
        print(f"✅ Respuesta: {respuesta[:100]}")
        resultado = enviar_mensaje(respuesta)
        print(f"📤 CallMeBot: {resultado}")
    except Exception as e:
        print(f"❌ ERROR: {traceback.format_exc()}")

    resp_twiml = MessagingResponse()
    resp_twiml.message("✅ Listo, revisá tu WhatsApp")
    return Response(content=str(resp_twiml), media_type="text/xml")



@app.post("/webhook")
async def webhook(
    Body: str = Form(default=""),
    From: str = Form(default=""),
    MediaUrl0: str = Form(default=""),
    MediaContentType0: str = Form(default="")
):
    mensaje = Body.strip()
    numero = From.strip()
    media_url = MediaUrl0.strip()
    media_type = MediaContentType0.strip()

    print(f"📩 De {numero}: {mensaje} | Media: {media_type}")

    try:
        # Audio
        if media_type.startswith("audio/"):
            from app.whatsapp import descargar_media
            from app.gemini import transcribir_audio
            audio_bytes = descargar_media(media_url)
            respuesta = transcribir_audio(audio_bytes, mime_type=media_type)

        # PDF
        elif media_type == "application/pdf":
            from app.whatsapp import descargar_media
            from app.gemini import analizar_pdf
            pdf_bytes = descargar_media(media_url)
            respuesta = analizar_pdf(pdf_bytes)

        # Texto normal
        else:
            respuesta = procesar_mensaje(mensaje)

        enviar_mensaje(respuesta)

    except Exception as e:
        print(f"❌ ERROR: {traceback.format_exc()}")

    resp_twiml = MessagingResponse()
    resp_twiml.message("✅ Listo, revisá tu WhatsApp")
    return Response(content=str(resp_twiml), media_type="text/xml")