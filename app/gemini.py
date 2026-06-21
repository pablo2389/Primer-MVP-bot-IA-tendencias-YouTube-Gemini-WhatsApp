import os
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("Falta GEMINI_API_KEY en el archivo .env")

client = genai.Client(api_key=GEMINI_API_KEY)


def analizar_tendencias(videos):
    if not videos:
        return "No hay suficientes datos para analizar."

    top = videos[:3]
    datos = "\n".join([
        f"#{i+1} | {v.get('titulo')} | {v.get('vistas'):,} vistas | {v.get('vistas_por_hora'):,}/hora | Score: {v.get('score_viral')} | {v.get('url')}"
        for i, v in enumerate(top)
    ])

    prompt = f"""
Sos un creador de contenido experto en YouTube Shorts y TikTok.
Estos son los 3 videos más virales de esta semana:

{datos}

Respondé en este formato para WhatsApp (sin markdown, solo emojis y texto):

🚀 TOP VIRAL DE LA SEMANA

1️⃣ [título]
📊 [vistas] vistas | [vistas/hora]/hora
🔗 [url]
💡 Por qué explota: [1 oración]
🎬 Cómo lo replicás: [1 oración]

2️⃣ ...
3️⃣ ...

🎯 GRABÁ ESTO HOY:
Título: [título ganador]
Hook: [frase de gancho 3 seg]
Guion: [guion 60 seg listo para grabar]
#️⃣ [5 hashtags]
"""
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return respuesta.text
    except Exception as e:
        return f"❌ Error Gemini: {str(e)}"


def respuesta_general(mensaje: str) -> str:
    prompt = f"""
Sos un asistente experto en marketing digital, redes sociales, SEO e IA.
Respondé desde WhatsApp: conciso, en español, con emojis, sin markdown complejo.
Máximo 300 palabras.

Mensaje: {mensaje}
"""
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        texto = respuesta.text
        return texto[:1500] if len(texto) > 1500 else texto
    except Exception as e:
        return f"❌ Error: {str(e)}"


def busqueda_web(pregunta: str) -> str:
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pregunta,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        texto = respuesta.text
        return texto[:1500] if len(texto) > 1500 else texto
    except Exception as e:
        return f"❌ Error búsqueda: {str(e)}"


def generar_imagen(descripcion: str) -> bytes | None:
    try:
        respuesta = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=descripcion,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1"
            )
        )
        imagen = respuesta.generated_images[0]
        return imagen.image.image_bytes
    except Exception as e:
        print(f"❌ Error imagen: {str(e)}")
        return None


def generar_ideas_posts(tema: str) -> str:
    prompt = f"""
Generá 5 ideas de posts para Instagram y TikTok sobre: {tema}

Para cada idea:
- Formato (Reel, Carrusel, Story, TikTok)
- Título gancho (menos de 10 palabras)
- Una línea de descripción

Concreto, creativo, orientado a engagement.
En español, formato WhatsApp con emojis, sin markdown.
"""
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        texto = respuesta.text
        return texto[:1500] if len(texto) > 1500 else texto
    except Exception as e:
        return f"❌ Error generando ideas: {str(e)}"


def transcribir_audio(audio_bytes: bytes, mime_type: str = "audio/ogg") -> str:
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                "Transcribí este audio en español. Si hay una pregunta, respondela también."
            ]
        )
        return respuesta.text
    except Exception as e:
        return f"❌ Error transcribiendo audio: {str(e)}"


def analizar_pdf(pdf_bytes: bytes) -> str:
    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                "Resumí este documento en español. Puntos clave, máximo 300 palabras, formato WhatsApp con emojis."
            ]
        )
        return respuesta.text
    except Exception as e:
        return f"❌ Error analizando PDF: {str(e)}"