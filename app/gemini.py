import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:
    raise Exception(
        "Falta GEMINI_API_KEY en el archivo .env"
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)



def analizar_tendencias(videos):


    if not videos:
        return "No hay suficientes datos para analizar."


    datos = "\n".join(
        [
            f"""
Título: {video.get('titulo', 'N/A')}
Canal: {video.get('canal', 'N/A')}
Vistas: {video.get('vistas', 'N/A')}
Likes: {video.get('likes', 'N/A')}
Comentarios: {video.get('comentarios', 'N/A')}
Vistas por hora: {video.get('vistas_por_hora', 'N/A')}
Score: {video.get('score_viral', 'N/A')}
Fecha: {video.get('fecha', 'N/A')}
URL: {video.get('url', 'N/A')}
"""
            for video in videos
        ]
    )


    prompt = f"""
Eres un analista profesional de oportunidades de contenido
y marketing digital.

Analizas tendencias de YouTube relacionadas con:

- SEO Local
- Google Business Profile
- WordPress
- React
- Inteligencia Artificial
- ChatGPT
- Marketing Digital
- Automatización para negocios


Tu objetivo es detectar oportunidades reales de contenido
basándote en los datos entregados.


Estos son los videos analizados:

{datos}



Devuelve EXACTAMENTE este formato:


🔥 OPORTUNIDAD DETECTADA


NIVEL DE OPORTUNIDAD:
(Alta / Media / Baja)


NICHO:
(nombre del nicho detectado)


POR QUÉ ESTÁ FUNCIONANDO:
(explicación corta basada en métricas reales)


PATRONES DETECTADOS:

- patrón 1
- patrón 2
- patrón 3


OPORTUNIDAD PARA NEGOCIOS:

(explica cómo podría aprovecharse esta tendencia
para una empresa, profesional o marca)


IDEA ORIGINAL DE CONTENIDO:

(no copies videos existentes)


TÍTULO RECOMENDADO:

(un título atractivo)


HOOK PRIMEROS 3 SEGUNDOS:

(frase inicial para captar atención)


GUION SHORT 60 SEGUNDOS:

(pequeño guion)


HASHTAGS:

#tag1 #tag2 #tag3



Reglas:

- No inventes métricas.
- No prometas resultados garantizados.
- No digas que una tendencia asegura ventas.
- Diferencia datos reales de hipótesis.
- Usa lenguaje profesional.
- Analiza patrones, no copies contenido.
- Prioriza oportunidades útiles para negocios reales.
"""


    try:

        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )


        return respuesta.text


    except Exception as e:

        return f"Error Gemini: {str(e)}"