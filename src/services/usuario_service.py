from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from models.usuario import Usuario
from flask import session
from werkzeug.security import check_password_hash
from database import db
from services.auth_service import hash_password


# --- REGISTRO DE USUARIO --- #
def crear_usuario(datos):
    """
    Crea un nuevo usuario en la base de datos.

    Hashea la contraseña y registra al usuario con los datos proporcionados.

    Args:
        datos (dict): Diccionario con claves 'nombre', 'apellidos', 'usuario', 'gmail', 'contrasena'.

    Returns:
        tuple: (bool, str) - Éxito y mensaje descriptivo.
    """
    try:
        # C7: usar siempre hash_password de auth_service para consistencia de algoritmo
        password_hashed = hash_password(datos["contrasena"])
        nuevo_usuario = Usuario(
            nombre=datos["nombre"],
            apellidos=datos["apellidos"],
            usuario=datos["usuario"],
            gmail=datos["gmail"],
            contrasena=password_hashed,
        )

        db.session.add(nuevo_usuario)

        db.session.commit()
        return True, "Registro completado con éxito."

    except Exception as e:
        db.session.rollback()
        print(f"!!! ERROR DE BD: {e}")
        return False, f"Error al registrar: {str(e)}"


def actualizar_contrasena(usuario_id, password_antiguo, nuevo_password):
    """
    Actualiza la contraseña de un usuario existente.

    Verifica la contraseña antigua antes de cambiarla.

    Args:
        usuario_id (int): ID del usuario.
        password_antiguo (str): Contraseña actual.
        nuevo_password (str): Nueva contraseña.

    Returns:
        bool: True si se actualizó correctamente, False en caso contrario.
    """
    usuario = Usuario.query.get(usuario_id)
    if usuario and check_password_hash(usuario.contrasena, password_antiguo):
        usuario.contrasena = hash_password(nuevo_password)
        db.session.commit()
        return True
    return False


# --- OBTENER PERFIL --- #
def obtener_perfil_completo(usuario_id):
    """
    Obtiene el perfil completo de un usuario por su ID.

    Args:
        usuario_id (int): ID del usuario.

    Returns:
        Usuario or None: Objeto Usuario si existe, None en caso contrario.
    """
    return Usuario.query.get(usuario_id)


def obtener_usuario_actual():
    usuario_id = session.get("usuario_id")
    if usuario_id:
        return Usuario.query.get(usuario_id)
    return None
