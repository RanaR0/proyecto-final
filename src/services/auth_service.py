from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from models import Usuario

# --- FUNCIONES DE CONTROL DE ACCESO ---


def login_usuario(identificador, password):

    # Buscamos por usuario o por gmail para dar flexibilidad al login
    usuario = Usuario.query.filter(
        (Usuario.usuario == identificador) | (Usuario.gmail == identificador)
    ).first()

    if usuario and check_password_hash(usuario.contrasena, password):
        # Guardamos datos mínimos en la sesión (cookie encriptada)
        session.clear()
        session["usuario_id"] = usuario.id
        session["nombre"] = usuario.nombre
        return usuario
    return None


def logout_usuario():
    session.clear()


def esta_autenticado():
    return "usuario_id" in session


# --- 2. FUNCIONES DE SEGURIDAD DE CUENTA ---

def hash_password(password_plano):
    return generate_password_hash(password_plano, method="pbkdf2:sha256")


# --- 3. FUNCIONES DE RECUPERACIÓN Y VALIDACIÓN ---


def verificar_disponibilidad(nombre_usuario, gmail):
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
