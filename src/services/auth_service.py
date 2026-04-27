from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from models import Usuario

# --- FUNCIONES DE CONTROL DE ACCESO ---


def login_usuario(identificador, password):
    """
    Autentica a un usuario mediante nombre de usuario o correo electrónico.

    Busca al usuario por 'usuario' o 'gmail', verifica la contraseña hasheada
    y establece la sesión si es correcta.

    Args:
        identificador (str): Nombre de usuario o correo electrónico.
        password (str): Contraseña en texto plano.

    Returns:
        dict: Diccionario con 'usuario' (objeto Usuario si exitoso) y 'error' (mensaje de error si falla).
    """
    # Buscamos por usuario o por gmail para dar flexibilidad al login
    usuario = Usuario.query.filter(
        (Usuario.usuario == identificador) | (Usuario.gmail == identificador)  # type: ignore
    ).first()

    if usuario and check_password_hash(usuario.contrasena, password):
        # Guardamos datos mínimos en la sesión (cookie encriptada)
        session.clear()
        session["usuario_id"] = usuario.id
        session["nombre"] = usuario.nombre
        return {"usuario": usuario, "error": None}
    elif usuario:
        return {"usuario": None, "error": "Contraseña incorrecta"}
    else:
        return {"usuario": None, "error": "Usuario no encontrado"}


def logout_usuario():
    """
    Cierra la sesión del usuario actual.

    Limpia todos los datos de la sesión de Flask.
    """
    session.clear()


def esta_autenticado():
    """
    Verifica si hay un usuario autenticado en la sesión actual.

    Returns:
        bool: True si hay un usuario_id en la sesión, False en caso contrario.
    """
    return "usuario_id" in session


# --- 2. FUNCIONES DE SEGURIDAD DE CUENTA ---


def hash_password(password_plano):
    """
    Genera un hash seguro para una contraseña.

    Utiliza PBKDF2 con SHA-256 para el hasheado.

    Args:
        password_plano (str): Contraseña en texto plano.

    Returns:
        str: Hash de la contraseña.
    """
    return generate_password_hash(password_plano, method="pbkdf2:sha256")


# --- 3. FUNCIONES DE RECUPERACIÓN Y VALIDACIÓN ---


def verificar_disponibilidad(nombre_usuario, gmail):
    """
    Verifica si un nombre de usuario y correo electrónico están disponibles.

    Args:
        nombre_usuario (str): Nombre de usuario a verificar.
        gmail (str): Correo electrónico a verificar.

    Returns:
        tuple: (bool, str) - Disponibilidad y mensaje descriptivo.
    """
    if Usuario.query.filter_by(usuario=nombre_usuario).first():
        return False, "El nombre de usuario ya está en uso."
    if Usuario.query.filter_by(gmail=gmail).first():
        return False, "El correo electrónico ya está registrado."
    return True, "Disponible"


def generar_token_recuperacion(gmail):
    import secrets

    usuario = Usuario.query.filter_by(gmail=gmail).first()
    if usuario:
        token = secrets.token_urlsafe(32)
        # Aquí guardarías el token en una tabla de 'Tokens' con fecha de expiración
        return token
    return None
