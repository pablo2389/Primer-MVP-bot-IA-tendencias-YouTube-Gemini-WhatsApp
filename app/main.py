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
async def webhook(Body: str = Form(default=""), From: str = Form(default="")):
    mensaje = Body.strip()
    numero = From.strip()
    print(f"📩 Mensaje de {numero}: {mensaje}")

    async def procesar_y_enviar():
        await asyncio.sleep(0.1)
        try:
            respuesta = procesar_mensaje(mensaje)
            print(f"✅ Respuesta generada: {respuesta[:100]}")
            resultado = enviar_mensaje(respuesta)
            print(f"📤 CallMeBot: {resultado}")
        except Exception as e:
            print(f"❌ ERROR COMPLETO: {traceback.format_exc()}")

    asyncio.create_task(procesar_y_enviar())

    resp_twiml = MessagingResponse()
    resp_twiml.message("⏳ Procesando tu consulta...")
    return Response(content=str(resp_twiml), media_type="text/xml")