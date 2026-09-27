import requests

def obtener_indicador_economico(moneda: str = "dolar") -> dict:
    """Obtiene tipos de cambio internacionales en tiempo real."""
    url = f"https://mindicador.cl/api/{moneda.lower()}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            valor = data['serie'][0]['valor']
            unidad = data['unidad_medida']
            return {"exito": True, "moneda": moneda, "valor": valor, "unidad": unidad}
        elif response.status_code == 404:
            return {"exito": False, "mensaje": f"Indicador '{moneda}' no encontrado (HTTP 404)."}
        else:
            return {"exito": False, "mensaje": f"Error del servidor externo (HTTP {response.status_code})."}
    except requests.exceptions.Timeout:
        return {"exito": False, "mensaje": "Tiempo de espera agotado al conectar con el servidor."}
    except requests.exceptions.RequestException as e:
        return {"exito": False, "mensaje": f"Error de red o conexión: {type(e).__name__}"}


def obtener_clima_santiago() -> dict:
    """Obtiene el clima meteorológico para decisiones operativas de proyectos."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=-33.45&longitude=-70.66&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data['current_weather']['temperature']
            wind = data['current_weather']['windspeed']
            return {"exito": True, "temperatura": temp, "viento": wind}
        return {"exito": False, "mensaje": f"Error HTTP {response.status_code}"}
    except requests.exceptions.RequestException:
        return {"exito": False, "mensaje": "Sin conexión al servicio meteorológico."}