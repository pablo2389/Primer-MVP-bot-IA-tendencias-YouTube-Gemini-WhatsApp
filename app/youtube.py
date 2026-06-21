import os

from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


if not YOUTUBE_API_KEY:
    raise Exception(
        "Falta YOUTUBE_API_KEY en el archivo .env"
    )


TEMAS = {
    "seo": '"local seo" OR "seo local"',
    "googlebusiness": '"google business profile"',
    "wordpress": '"wordpress tutorial"',
    "react": '"react js tutorial"',
    "chatgpt": '"chatgpt tutorial"',
}



def buscar_videos(query, max_results=20):

    query_real = TEMAS.get(
        query.lower(),
        query
    )


    youtube = build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY
    )


    fecha_limite = (
        datetime.now(timezone.utc)
        - timedelta(days=7)
    ).isoformat()



    search_response = youtube.search().list(
        q=query_real,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="date",
        publishedAfter=fecha_limite,
        videoDuration="any"
    ).execute()



    ids = [
        item["id"]["videoId"]
        for item in search_response.get("items", [])
    ]


    if not ids:
        return []



    stats_response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(ids)
    ).execute()



    resultados = []


    palabras_basura = [

        "subscribe",
        "abone",
        "follow",
        "like",
        "share",
        "status",
        "live",
        "music",
        "dance",
        "song",
        "comedy",
        "funny",
        "prank",
        "gaming",
        "minecraft",
        "fortnite",
        "pokemon",
        "movie",
        "trailer",
        "reaction"

    ]



    for video in stats_response.get("items", []):


        stats = video.get(
            "statistics",
            {}
        )


        snippet = video.get(
            "snippet",
            {}
        )


        titulo = snippet.get(
            "title",
            ""
        ).lower()



        if any(
            palabra in titulo
            for palabra in palabras_basura
        ):
            continue



        vistas = int(
            stats.get(
                "viewCount",
                0
            )
        )


        likes = int(
            stats.get(
                "likeCount",
                0
            )
        )


        comentarios = int(
            stats.get(
                "commentCount",
                0
            )
        )



        if vistas < 500:
            continue



        fecha = snippet.get(
            "publishedAt"
        )


        fecha_video = datetime.fromisoformat(
            fecha.replace(
                "Z",
                "+00:00"
            )
        )



        horas = (
            datetime.now(timezone.utc)
            - fecha_video
        ).total_seconds() / 3600



        if horas < 1:
            horas = 1



        vistas_por_hora = round(
            vistas / horas
        )



        score = round(
            (vistas_por_hora * 0.7)
            +
            (likes * 0.2)
            +
            (comentarios * 0.1)
        )



        resultados.append({

            "id": video.get("id"),

            "titulo": snippet.get(
                "title"
            ),

            "canal": snippet.get(
                "channelTitle"
            ),

            "url": 
            f"https://youtube.com/watch?v={video.get('id')}",


            "miniatura":
            snippet.get(
                "thumbnails",
                {}
            )
            .get(
                "high",
                {}
            )
            .get(
                "url"
            ),


            "vistas": vistas,

            "likes": likes,

            "comentarios": comentarios,

            "fecha": fecha,

            "horas_publicado": round(
                horas
            ),

            "vistas_por_hora": vistas_por_hora,

            "score_viral": score

        })



    resultados.sort(
        key=lambda x: x["score_viral"],
        reverse=True
    )


    return resultados




def buscar_canal(nombre_canal: str, max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Primero busca el canal
    canal_response = youtube.search().list(
        q=nombre_canal,
        part="snippet",
        type="channel",
        maxResults=1
    ).execute()

    items = canal_response.get("items", [])
    if not items:
        return []

    channel_id = items[0]["id"]["channelId"]

    # Busca los videos más recientes del canal
    search_response = youtube.search().list(
        channelId=channel_id,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="viewCount"
    ).execute()

    ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
    if not ids:
        return []

    stats_response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(ids)
    ).execute()

    resultados = []
    for video in stats_response.get("items", []):
        stats = video.get("statistics", {})
        snippet = video.get("snippet", {})
        resultados.append({
            "id": video.get("id"),
            "titulo": snippet.get("title"),
            "canal": snippet.get("channelTitle"),
            "url": f"https://youtube.com/watch?v={video.get('id')}",
            "vistas": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comentarios": int(stats.get("commentCount", 0)),
            "fecha": snippet.get("publishedAt"),
        })

    resultados.sort(key=lambda x: x["vistas"], reverse=True)
    return resultados