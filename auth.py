 # Autenticación y Cifrado de Credenciales (U3 - Paso 2)

import hashlib

# Usuarios administradores guardados con Hash SHA-256
USUARIOS_DB = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "gerente": hashlib.sha256("ecotech2026".encode()).hexdigest()
}

def encriptar_password(password: str) -> str:
    """Aplica algoritmo de cifrado Hash SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def autenticar_usuario(usuario: str, password_ingresada: str) -> bool:
    """Valida credenciales protegiendo frente a valores nulos o incorrectos."""
    if not usuario or not password_ingresada:
        return False
    
    hash_ingresado = encriptar_password(password_ingresada)
    hash_almacenado = USUARIOS_DB.get(usuario)
    return hash_almacenado is not None and hash_almacenado == hash_ingresado