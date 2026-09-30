"""Funciones de validación para los datos ingresados por el usuario."""
# Este archivo contiene funciones que revisan si los datos
# ingresados por el usuario son correctos antes de guardarlos.


import re
# Importamos "re", que permite trabajar con expresiones regulares.
# Se utiliza principalmente para validar el formato del correo.


from datetime import datetime
# Importamos "datetime" para poder comprobar si una fecha
# tiene un formato válido.


def validar_nombre(nombre: str) -> bool:
    # Esta función recibe un nombre y devuelve True o False.
    # True = el nombre es válido.
    # False = el nombre no es válido.

    """Valida que el nombre no esté vacío."""
    # Es una descripción de lo que hace la función.

    if not nombre:
        # Si "nombre" está vacío, se ejecuta esta condición.

        return False
        # False significa que el nombre NO es válido.

    return bool(nombre.strip())
    # strip() elimina espacios al principio y al final.
    # bool() convierte el resultado en True o False.
    #
    # Ejemplo:
    # "Carmen"       -> True
    # "   Carmen   " -> True
    # "     "        -> False


def validar_correo(correo: str) -> bool:
    # Esta función revisa si el correo tiene un formato básico válido.

    """Valida el formato básico del correo electrónico."""

    if not correo:
        # Si el correo está vacío...

        return False
        # ...el correo no es válido.

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    # Creamos un patrón para revisar el formato del correo.
    #
    # Busca una estructura parecida a:
    # nombre@dominio.cl
    #
    # Por ejemplo:
    # carmen@ecotech.cl -> válido
    # juan@gmail.com    -> válido
    #
    # La expresión regular comprueba que:
    # - exista texto antes del @
    # - exista un @
    # - exista texto después del @
    # - exista un punto
    # - exista texto después del punto

    return bool(re.match(patron, correo.strip()))
    # re.match() compara el correo con el patrón.
    # strip() elimina espacios innecesarios.
    # bool() transforma el resultado en True o False.


def validar_fecha(fecha: str) -> bool:
    # Esta función comprueba que la fecha tenga un formato válido.

    """Valida que la fecha exista y utilice el formato YYYY-MM-DD."""

    if not fecha:
        # Si no se ingresó ninguna fecha...

        return False
        # ...la fecha no es válida.

    try:
        # try permite intentar ejecutar un código
        # que podría producir un error.

        datetime.strptime(fecha.strip(), "%Y-%m-%d")
        # strptime() intenta convertir el texto a una fecha.
        #
        # "%Y-%m-%d" significa:
        # %Y = año con 4 números
        # %m = mes con 2 números
        # %d = día con 2 números
        #
        # Ejemplo válido:
        # 2026-08-26

        return True
        # Si la fecha se puede convertir correctamente,
        # significa que es válida.

    except ValueError:
        # Si la fecha tiene un formato incorrecto
        # o no existe, se produce un ValueError.

        return False
        # En ese caso indicamos que la fecha no es válida.


def validar_salario(salario: float) -> bool:
    # Esta función recibe un salario y comprueba que sea mayor que cero.

    """Valida que el salario sea mayor que cero."""

    return salario > 0
    # Si el salario es mayor que 0 devuelve True.
    #
    # Ejemplo:
    # 1200000 -> True
    # 0       -> False
    # -500000 -> False


def validar_cargo(cargo: str) -> bool:
    # Esta función comprueba que el cargo no esté vacío.

    """Valida que el cargo no esté vacío."""

    if not cargo:
        # Si no se ingresó ningún cargo...

        return False
        # ...el cargo no es válido.

    return bool(cargo.strip())
    # Elimina espacios al principio y al final
    # y comprueba si todavía queda algún texto.
    #
    # Ejemplo:
    # "Analista" -> True
    # "Desarrollador" -> True
    # "   " -> False