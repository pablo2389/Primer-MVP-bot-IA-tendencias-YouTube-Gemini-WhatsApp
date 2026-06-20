from app.youtube import buscar_videos
from app.gemini import analizar_tendencias, respuesta_general

MENU = """
🤖 *Bot IA - Tu asistente de contenido*

Comandos disponibles:

🔍 *tendencias [tema]*
Ej: tendencias inteligencia artificial

📝 *guion [tema]*
Ej: guion SEO local

💬 *cualquier pregunta*
Ej: cómo mejorar mi perfil de Google Business

📋 *ayuda* - muestra este menú
""".strip()


def procesar_mensaje(mensaje: str) -> str:
    texto = mensaje.strip()
    lower = texto.lower()

    # Menú
    if lower in ["ayuda", "help", "hola", "menu", "menú", "inicio", "start", "hi"]:
        return MENU

    # Tendencias YouTube
    if lower.startswith("tendencias"):
        partes = texto.split(" ", 1)
        tema = partes[1].strip() if len(partes) > 1 else "inteligencia artificial"
        return buscar_y_analizar(tema)

    # Guion específico
    if lower.startswith("guion"):
        partes = texto.split(" ", 1)
        tema = partes[1].strip() if len(partes) > 1 else "marketing digital"
        return generar_guion(tema)

    # Todo lo demás → asistente general con Gemini
    return respuesta_general(texto)


def buscar_y_analizar(tema: str) -> str:
    try:
        print(f"🔎 Buscando tendencias: {tema}")
        videos = buscar_videos(tema)
        if not videos:
            return f"⚠️ No encontré videos trending sobre *{tema}*. Probá con otro tema."
        analisis = analizar_tendencias(videos)
        return analisis[:1500] if len(analisis) > 1500 else analisis
    except Exception as e:
        return f"❌ Error buscando tendencias: {str(e)}"


def generar_guion(tema: str) -> str:
    try:
        videos = buscar_videos(tema, max_results=3)
        analisis = analizar_tendencias(videos)
        # Extraer solo la parte del guion
        if "GUION SHORT" in analisis:
            inicio = analisis.find("GUION SHORT")
            fin = analisis.find("HASHTAGS", inicio)
            guion = analisis[inicio:fin].strip() if fin != -1 else analisis[inicio:].strip()
            return f"📝 *{tema.upper()}*\n\n{guion}"
        return analisis[:1500]
    except Exception as e:
        return f"❌ Error generando guion: {str(e)}"