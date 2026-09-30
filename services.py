"""Servicios externos utilizados por EcoTech Solutions."""
# Este archivo contiene funciones que permiten obtener
# información desde servicios externos (APIs).


import requests
# "requests" permite hacer solicitudes HTTP desde Python.
# En palabras simples: permite que nuestro programa
# se comunique con páginas o servicios de Internet.


# Monedas permitidas para consultas económicas
MONEDAS_PERMITIDAS = {"dolar", "euro", "uf"}
# Creamos un conjunto (set) con las monedas que nuestro
# programa permite consultar.
#
# Solo se aceptan:
# - dolar
# - euro
# - uf


def validar_moneda(moneda: str) -> bool:
    # Esta función comprueba si la moneda ingresada
    # está dentro de las opciones permitidas.

    """Valida que la moneda ingresada esté permitida."""

    if not moneda:
        # Si no se ingresó ninguna moneda...

        return False
        # ...la moneda no es válida.

    moneda = moneda.strip().lower()
    # strip() elimina espacios al principio y al final.
    # lower() convierte todo a minúsculas.
    #
    # Ejemplo:
    # "  DOLAR  " -> "dolar"

    return moneda in MONEDAS_PERMITIDAS
    # "in" pregunta si la moneda está dentro del conjunto.
    #
    # Si está:
    # True
    #
    # Si no está:
    # False


def obtener_indicador_economico(moneda: str = "dolar") -> dict:
    # Esta función obtiene desde Internet el valor
    # de un indicador económico.
    #
    # Por defecto consulta el dólar.
    #
    # ": dict" significa que devuelve un diccionario.

    """Obtiene el valor actual de un indicador económico."""

    moneda = moneda.strip().lower()
    # Eliminamos espacios y convertimos la moneda
    # a minúsculas.


    if not validar_moneda(moneda):
        # Comprobamos si la moneda está permitida.

        return {
            "exito": False,
            "mensaje": (
                "Moneda no válida. "
                "Las opciones permitidas son: dolar, euro o uf."
            ),
        }
        # Si la moneda no está permitida,
        # devolvemos un mensaje de error.


    url = f"https://mindicador.cl/api/{moneda}"
    # Creamos la dirección de la API.
    #
    # Si moneda = "dolar":
    # https://mindicador.cl/api/dolar
    #
    # Si moneda = "euro":
    # https://mindicador.cl/api/euro
    #
    # La "f" permite insertar la variable
    # dentro del texto.


    try:
        # Intentamos conectarnos al servicio externo.


        response = requests.get(url, timeout=5)
        # requests.get() realiza una solicitud GET.
        #
        # timeout=5 significa que el programa esperará
        # como máximo 5 segundos por una respuesta.


        if response.status_code == 200:
            # HTTP 200 significa que la solicitud
            # fue procesada correctamente.

            data = response.json()
            # Convierte la respuesta de la API
            # desde JSON a un diccionario de Python.


            serie = data.get("serie")
            # Busca dentro de la respuesta los datos
            # asociados a "serie".


            unidad = data.get("unidad_medida")
            # Obtiene la unidad de medida del indicador.


            if not serie or unidad is None:
                # Comprueba si faltan datos importantes.

                return {
                    "exito": False,
                    "mensaje": "La API entregó datos incompletos.",
                }


            valor = serie[0].get("valor")
            # Obtiene el valor del primer registro de la serie.
            #
            # serie[0] = primer elemento.
            # get("valor") = obtiene su valor económico.


            if valor is None:
                # Comprueba si se encontró realmente un valor.

                return {
                    "exito": False,
                    "mensaje": "No se encontró el valor del indicador.",
                }


            return {
                "exito": True,
                "moneda": moneda,
                "valor": valor,
                "unidad": unidad,
            }
            # Si todo salió bien, devuelve los datos
            # del indicador económico.


        if response.status_code == 404:
            # HTTP 404 significa que el recurso solicitado
            # no fue encontrado.

            return {
                "exito": False,
                "mensaje": (
                    f"Indicador '{moneda}' no encontrado "
                    "(HTTP 404)."
                ),
            }


        return {
            "exito": False,
            "mensaje": (
                "Error del servidor externo "
                f"(HTTP {response.status_code})."
            ),
        }
        # Si ocurre otro código HTTP diferente de 200 o 404,
        # informamos que hubo un error del servicio.


    except requests.exceptions.Timeout:
        # Captura el error cuando el servidor tarda
        # demasiado en responder.

        return {
            "exito": False,
            "mensaje": (
                "Tiempo de espera agotado al conectar "
                "con el servidor."
            ),
        }


    except requests.exceptions.RequestException:
        # Captura otros errores relacionados con
        # la conexión HTTP.

        return {
            "exito": False,
            "mensaje": (
                "No fue posible conectarse al "
                "servicio económico."
            ),
        }


    except (ValueError, TypeError, KeyError, IndexError):
        # Captura errores cuando los datos recibidos
        # desde la API no tienen el formato esperado.

        return {
            "exito": False,
            "mensaje": (
                "La respuesta del servicio económico "
                "tiene un formato inesperado."
            ),
        }


def interpretar_codigo_clima(codigo: int) -> str:
    # Esta función recibe un código numérico del clima
    # y lo convierte en una descripción que una persona
    # pueda entender.

    """Convierte un código meteorológico WMO en una descripción."""

    estados = {
        # Diccionario que relaciona cada código
        # con una descripción del estado del tiempo.

        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        56: "Llovizna helada ligera",
        57: "Llovizna helada intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        66: "Lluvia helada ligera",
        67: "Lluvia helada intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        77: "Granos de nieve",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos intensos",
        85: "Chubascos de nieve ligeros",
        86: "Chubascos de nieve intensos",
        95: "Tormenta",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo intenso",
    }


    return estados.get(codigo, "Estado meteorológico desconocido")
    # Busca el código dentro del diccionario.
    #
    # Si lo encuentra, devuelve su descripción.
    #
    # Si no lo encuentra, devuelve:
    # "Estado meteorológico desconocido"


def obtener_clima_santiago() -> dict:
    # Esta función obtiene información meteorológica
    # actual para Santiago.

    """Obtiene las condiciones meteorológicas actuales de Santiago."""


    url = "https://api.open-meteo.com/v1/forecast"
    # Dirección de la API meteorológica.


    parametros = {
        # Parámetros que enviaremos a la API.

        "latitude": -33.45,
        # Latitud aproximada de Santiago.

        "longitude": -70.66,
        # Longitud aproximada de Santiago.

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        # Indicamos qué información queremos obtener:
        #
        # temperature_2m = temperatura
        # relative_humidity_2m = humedad
        # weather_code = código del clima
        # wind_speed_10m = velocidad del viento

        "timezone": "America/Santiago",
        # Indicamos la zona horaria de Santiago.
    }


    try:
        # Intentamos conectarnos con la API.


        response = requests.get(
            url,
            params=parametros,
            timeout=5,
        )
        # Realizamos la solicitud.
        #
        # params contiene los parámetros que queremos enviar.
        # timeout=5 limita la espera a 5 segundos.


        if response.status_code != 200:
            # Si el código no es 200, significa que hubo
            # algún problema con la solicitud.

            return {
                "exito": False,
                "mensaje": (
                    "Error del servicio meteorológico "
                    f"(HTTP {response.status_code})."
                ),
            }


        data = response.json()
        # Convertimos la respuesta JSON
        # en un diccionario de Python.


        datos_actuales = data.get("current")
        # Obtenemos la información meteorológica actual.


        if not isinstance(datos_actuales, dict):
            # Comprobamos que "datos_actuales" realmente
            # sea un diccionario.

            return {
                "exito": False,
                "mensaje": (
                    "La API meteorológica entregó "
                    "datos incompletos."
                ),
            }


        temperatura = datos_actuales.get("temperature_2m")
        # Obtenemos la temperatura.


        humedad = datos_actuales.get("relative_humidity_2m")
        # Obtenemos la humedad.


        codigo_clima = datos_actuales.get("weather_code")
        # Obtenemos el código que representa
        # el estado del clima.


        viento = datos_actuales.get("wind_speed_10m")
        # Obtenemos la velocidad del viento.


        if (
            temperatura is None
            or humedad is None
            or codigo_clima is None
        ):
            # Comprobamos que existan los datos principales.
            #
            # "or" significa "o".
            # Si falta cualquiera de estos datos,
            # se genera un mensaje de error.

            return {
                "exito": False,
                "mensaje": (
                    "No fue posible obtener todos los "
                    "datos meteorológicos requeridos."
                ),
            }


        estado = interpretar_codigo_clima(
            int(codigo_clima)
        )
        # Convertimos el código climático a número
        # y lo enviamos a la función
        # interpretar_codigo_clima().
        #
        # Por ejemplo:
        # 3 -> "Nublado"


        return {
            "exito": True,
            "temperatura": temperatura,
            "humedad": humedad,
            "estado": estado,
            "viento": viento,
        }
        # Devolvemos toda la información meteorológica.


    except requests.exceptions.Timeout:
        # Error cuando la API demora demasiado
        # en responder.

        return {
            "exito": False,
            "mensaje": (
                "El servicio meteorológico tardó "
                "demasiado en responder."
            ),
        }


    except requests.exceptions.RequestException:
        # Error general de conexión con la API.

        return {
            "exito": False,
            "mensaje": (
                "No fue posible conectarse al "
                "servicio meteorológico."
            ),
        }


    except (ValueError, TypeError, KeyError):
        # Captura errores relacionados con los datos
        # recibidos desde la API.

        return {
            "exito": False,
            "mensaje": (
                "La respuesta meteorológica tiene "
                "un formato inesperado."
            ),
        }