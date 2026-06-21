import os

from dotenv import load_dotenv
from google import genai


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
Tu trabajo es analizar qué videos están explotando ahora mismo
y decirle a otro creador exactamente cómo replicarlo.

Estos son los 3 videos más virales de esta semana:

{datos}

Respondé en este formato exacto para WhatsApp (sin markdown, solo emojis y texto):

🚀 TOP VIRAL DE LA SEMANA

1️⃣ [título del video #1]
📊 [vistas] vistas | [vistas/hora]/hora
🔗 [url]
💡 Por qué explota: [1 oración directa]
🎬 Cómo lo replicás: [1 oración concreta]

2️⃣ [título del video #2]
📊 [vistas] vistas | [vistas/hora]/hora
🔗 [url]
💡 Por qué explota: [1 oración directa]
🎬 Cómo lo replicás: [1 oración concreta]

3️⃣ [título del video #3]
📊 [vistas] vistas | [vistas/hora]/hora
🔗 [url]
💡 Por qué explota: [1 oración directa]
🎬 Cómo lo replicás: [1 oración concreta]

---
🎯 GRABÁ ESTO HOY:
Título: [título ganador para tu canal]
Hook (primeros 3 seg): [frase de gancho]
Guion (60 seg): [guion listo para grabar, natural y directo]
#️⃣ [5 hashtags relevantes]
"""

    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return respuesta.text

    except Exception as e:
        return f"Error Gemini: {str(e)}"


def respuesta_general(mensaje: str) -> str:

    prompt = f"""
Sos un asistente experto en marketing digital, contenido para redes sociales,
SEO, inteligencia artificial aplicada a negocios, y estrategia de contenido
para YouTube, TikTok e Instagram.

El usuario te escribe desde WhatsApp. Respondé de forma:
- Concisa y clara (máximo 300 palabras)
- En español
- Con emojis cuando ayuden a la lectura
- Sin markdown complejo (sin ** ni #, solo texto plano y emojis)
- Directo al punto, sin rodeos

Mensaje del usuario: {mensaje}
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


def generar_ideas_posts(tema: str) -> str:

    prompt = f"""
Generá 5 ideas de posts para Instagram y TikTok sobre el tema: {tema}

Para cada idea incluí:
- Formato (Reel, Carrusel, Story, TikTok)
- Título gancho (menos de 10 palabras)
- Una línea de descripción

Sé concreto, creativo y orientado a engagement.
Respondé en español, formato limpio para WhatsApp con emojis.
Sin markdown complejo, solo texto y emojis.
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