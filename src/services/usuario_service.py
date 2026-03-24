from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from models.usuario import Usuario
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from services.auth_service import hash_password


# --- REGISTRO DE USUARIO --- #
def crear_usuario(datos):

    try:
        # 1. Hashear la contraseña
        password_hashed = generate_password_hash(
            datos["contrasena"], method="pbkdf2:sha256"
        )

        # 2. Crear instancia de Usuario
        nuevo_usuario = Usuario(
            nombre=datos["nombre"],  # type: ignore
            apellidos=datos["apellidos"],  # type: ignore
            usuario=datos["usuario"],  # type: ignore
            contrasena=password_hashed,  # type: ignore
            gmail=datos["gmail"],  # type: ignore
        )

        db.session.add(nuevo_usuario)

        # 4. Guardar en base de datos
        db.session.commit()
        return True, "Registro completado con éxito."

    except Exception as e:
        db.session.rollback()  # Si algo falla, deshace los cambios
        return False, f"Error al registrar: {str(e)}"


def actualizar_contrasena(usuario_id, password_antiguo, nuevo_password):

    usuario = Usuario.query.get(usuario_id)
    if usuario and check_password_hash(usuario.contrasena, password_antiguo):
        usuario.contrasena = hash_password(nuevo_password)
        db.session.commit()
        return True
    return False


# --- OBTENER PERFIL --- #
def obtener_perfil_completo(usuario_id):
    return Usuario.query.get(usuario_id)


def obtener_usuario_actual():
    usuario_id = session.get("usuario_id")
    if usuario_id:
        return Usuario.query.get(usuario_id)
    return None