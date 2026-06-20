from fastapi import FastAPI

from app.whatsapp import enviar_mensaje
from app.youtube import buscar_videos
from app.gemini import analizar_tendencias


app = FastAPI()


@app.get("/")
def inicio():
    return {
        "mensaje": "Bot IA WhatsApp funcionando 🚀"
    }


@app.get("/test-whatsapp")
def test_whatsapp():

    resultado = enviar_mensaje(
        "🤖 Bot conectado correctamente desde Python"
    )

    return {
        "respuesta": resultado
    }


@app.get("/trending")
def trending(tema: str = "seo"):

    videos = buscar_videos(tema)

    return {
        "tema": tema,
        "videos": videos
    }


@app.get("/ideas")
def ideas(tema: str = "seo"):

    videos = buscar_videos(tema)

    analisis = analizar_tendencias(videos)

    return {
        "tema": tema,
        "analisis": analisis
    }


@app.get("/viral")
def viral(tema: str = "seo"):

    videos = buscar_videos(tema)

    analisis = analizar_tendencias(videos)

    return {
        "tema": tema,
        "resultado": analisis
    }


@app.get("/whatsapp-viral")
def whatsapp_viral(tema: str = "seo"):

    videos = buscar_videos(tema)

    analisis = analizar_tendencias(videos)

    try:
        enviar_mensaje(analisis)
        whatsapp = "enviado correctamente"

    except Exception as e:
        whatsapp = f"error whatsapp: {str(e)}"


    return {
        "ok": True,
        "tema": tema,
        "whatsapp": whatsapp
    }


@app.get("/descubrir")
def descubrir():

    nichos = [
        "google business",
        "seo local",
        "chatgpt",
        "inteligencia artificial",
        "wordpress",
        "react",
        "marketing digital",
        "youtube shorts"
    ]


    resultado = {}


    for nicho in nichos:

        try:

            videos = buscar_videos(
                nicho,
                max_results=30
            )

            resultado[nicho] = videos[:5]


        except Exception as e:

            resultado[nicho] = {
                "error": str(e)
            }


    return resultado



@app.get("/oportunidad")
def oportunidad():

    videos = []


    nichos = [
        "google business",
        "seo local",
        "chatgpt",
        "inteligencia artificial",
        "wordpress",
        "react"
    ]


    for nicho in nichos:

        try:

            videos.extend(
                buscar_videos(
                    nicho,
                    max_results=10
                )
            )


        except Exception as e:

            print(
                f"Error en {nicho}: {e}"
            )



    videos.sort(
        key=lambda x: x["score_viral"],
        reverse=True
    )


    top = videos[:20]


    analisis = analizar_tendencias(top)


    return {
        "videos": top,
        "analisis": analisis
    }