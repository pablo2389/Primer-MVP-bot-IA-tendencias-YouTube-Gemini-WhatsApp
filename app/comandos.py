from app.youtube import buscar_videos, buscar_canal
from app.gemini import respuesta_general, generar_ideas_posts

MENU = """
🤖 *Bot IA - Tu asistente de contenido*

Comandos disponibles:

🔍 *tendencias [tema]*
Ej: tendencias ferrari

📝 *guion [tema]*
Ej: guion SEO local

💡 *ideas [tema]*
Ej: ideas restaurante vegano

📺 *canal [nombre]*
Ej: canal MrBeast

💬 *cualquier pregunta con ?*
Ej: cómo mejorar mi perfil de Google Business

📋 *ayuda* - muestra este menú
""".strip()


def procesar_mensaje(mensaje: str) -> str:
    texto = mensaje.strip()
    lower = texto.lower()

    if lower in ["ayuda", "help", "hola", "menu", "menú", "inicio", "start", "hi"]:
        return MENU

    if lower.startswith("tendencias"):
        partes = texto.split(" ", 1)
        tema = partes[1].strip() if len(partes) > 1 else "inteligencia artificial"
        return buscar_y_analizar(tema)

    if lower.startswith("guion"):
        partes = texto.split(" ", 1)
        tema = partes[1].strip() if len(partes) > 1 else "marketing digital"
        return generar_guion(tema)

    if lower.startswith("ideas"):
        partes = texto.split(" ", 1)
        tema = partes[1].strip() if len(partes) > 1 else "marketing digital"
        return ideas_posts(tema)

    if lower.startswith("canal"):
        partes = texto.split(" ", 1)
        nombre = partes[1].strip() if len(partes) > 1 else ""
        if not nombre:
            return "⚠️ Escribí el nombre del canal. Ej: *canal MrBeast*"
        return analizar_canal(nombre)

    if "?" in texto:
        return respuesta_general(texto)

    return buscar_y_analizar(texto)


# ── Tendencias ────────────────────────────────────────────

def buscar_y_analizar(tema: str) -> str:
    try:
        videos = buscar_videos(tema)
        if not videos:
            return f"⚠️ No encontré videos sobre *{tema}*."
        return formatear_videos_corto(videos, tema)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def formatear_videos_corto(videos: list, tema: str) -> str:
    lineas = [f"🔥 *Top videos — {tema.upper()}*\n"]
    for i, v in enumerate(videos[:5], 1):
        fecha = v["fecha"][:10]
        lineas.append(
            f"{i}. *{v['titulo']}*\n"
            f"   👁 {v['vistas']:,} vistas · 📅 {fecha}\n"
            f"   🔗 {v['url']}\n"
        )
    return "\n".join(lineas)


# ── Guion ─────────────────────────────────────────────────

def generar_guion(tema: str) -> str:
    try:
        from app.gemini import analizar_tendencias
        videos = buscar_videos(tema, max_results=3)
        analisis = analizar_tendencias(videos)
        if "GUION SHORT" in analisis:
            inicio = analisis.find("GUION SHORT")
            fin = analisis.find("HASHTAGS", inicio)
            guion = analisis[inicio:fin].strip() if fin != -1 else analisis[inicio:].strip()
            return f"📝 *{tema.upper()}*\n\n{guion}"
        return analisis[:1500]
    except Exception as e:
        return f"❌ Error generando guion: {str(e)}"


# ── Ideas Instagram/TikTok ────────────────────────────────

def ideas_posts(tema: str) -> str:
    try:
        ideas = generar_ideas_posts(tema)
        return ideas
    except Exception as e:
        return f"❌ Error generando ideas: {str(e)}"


# ── Análisis de canal ─────────────────────────────────────

def analizar_canal(nombre: str) -> str:
    try:
        videos = buscar_canal(nombre)
        if not videos:
            return f"⚠️ No encontré el canal *{nombre}*."

        lineas = [f"📺 *Canal — {nombre.upper()}*\n"]
        for i, v in enumerate(videos[:5], 1):
            fecha = v["fecha"][:10]
            lineas.append(
                f"{i}. *{v['titulo']}*\n"
                f"   👁 {v['vistas']:,} vistas · ❤️ {v['likes']:,} likes · 📅 {fecha}\n"
                f"   🔗 {v['url']}\n"
            )
        return "\n".join(lineas)
    except Exception as e:
        return f"❌ Error analizando canal: {str(e)}"