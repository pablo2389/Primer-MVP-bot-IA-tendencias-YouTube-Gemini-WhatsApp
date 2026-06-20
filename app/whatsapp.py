import os
import requests

from dotenv import load_dotenv


load_dotenv()



CALLMEBOT_PHONE = os.getenv(
    "CALLMEBOT_PHONE"
)

CALLMEBOT_APIKEY = os.getenv(
    "CALLMEBOT_APIKEY"
)



if not CALLMEBOT_PHONE or not CALLMEBOT_APIKEY:
    raise Exception(
        "Faltan variables CALLMEBOT_PHONE o CALLMEBOT_APIKEY en .env"
    )



def enviar_mensaje(texto):

    url = "https://api.callmebot.com/whatsapp.php"


    params = {
        "phone": CALLMEBOT_PHONE,
        "text": texto,
        "apikey": CALLMEBOT_APIKEY
    }


    try:

        respuesta = requests.get(
            url,
            params=params,
            timeout=10
        )


        respuesta.raise_for_status()


        return {
            "estado": "enviado",
            "respuesta": respuesta.text
        }



    except requests.exceptions.RequestException as e:

        return {
            "estado": "error",
            "mensaje": str(e)
        }