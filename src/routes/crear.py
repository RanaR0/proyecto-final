from flask import Blueprint, render_template, request, redirect, url_for, flash
from urllib.parse import urlencode
from models.receta import Receta
from models.pasos import Paso
from models.foto import Foto
from models.receta_ingrediente import Receta_Ingrediente
from models.ingrediente import Ingrediente
from database import db
from services import obtener_usuario_actual
import os
import uuid

from utils.data_utils import (
    save_uploaded_file,
    get_static_root,
    get_user_folder,
    get_recipe_folder,
    get_steps_folder,
    ensure_folder_exists,
)

crear_bp = Blueprint("crear", __name__)

# -----------------------------
# CONFIGURACIÓN
# -----------------------------

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_TITLE_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 500


# -----------------------------
# HELPERS
# -----------------------------

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_image(file_obj, file_name):
    if not file_obj or not file_name:
        return True, ""

    if not allowed_file(file_name):
        return False, (
            f"Tipo de archivo no permitido. "
            f"Solo se aceptan: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    file_obj.seek(0)

    if file_size > MAX_FILE_SIZE:
        return False, "La imagen supera el máximo permitido (5MB)."

    return True, ""

def validate_ingredients(ingredientes):
    """
    Valida la lista de ingredientes.

    Returns:
        (bool, str) - (Es válido, mensaje de error si aplica)
    """
    ingredientes_validos = [ing.strip() for ing in ingredientes if ing.strip()]

    if not ingredientes_validos:
        return False, "Debes agregar al menos un ingrediente."

    return True, ""

def validate_form_data(nombre, descripcion, tiempo, raciones, categoria):
    if not nombre.strip():
        return False, "El título de la receta es obligatorio."

    if len(nombre.strip()) > MAX_TITLE_LENGTH:
        return False, (
            f"El título no puede exceder {MAX_TITLE_LENGTH} caracteres."
        )

    if not descripcion.strip():
        return False, "La descripción es obligatoria."

    if len(descripcion.strip()) > MAX_DESCRIPTION_LENGTH:
        return False, (
            f"La descripción no puede exceder "
            f"{MAX_DESCRIPTION_LENGTH} caracteres."
        )

    if not raciones:
        return False, "Las porciones son obligatorias."

    try:
        int(raciones)
    except (ValueError, TypeError):
        return False, "Las porciones deben ser numéricas."

    if tiempo:
        try:
            int(tiempo)
        except (ValueError, TypeError):
            return False, "El tiempo debe ser numérico."

    if not categoria:
        return False, "La categoría es obligatoria."

    return True, ""

def validate_steps(pasos_texto):
    """
    Valida la lista de pasos.

    Returns:
        (bool, str) - (Es válido, mensaje de error si aplica)
    """
    pasos_validos = [paso.strip() for paso in pasos_texto if paso.strip()]

    if not pasos_validos:
        return False, "Debes agregar al menos un paso de instrucciones."

    return True, ""

def retorno_con_error(
    nombre,
    descripcion,
    tiempo,
    raciones,
    categoria,
    ingredientes,
    pasos,
    mensaje_error,
):
    params = [
        ("titulo", nombre),
        ("descripcion", descripcion),
        ("tiempo", tiempo),
        ("raciones", raciones),
        ("categoria", categoria),
        ("error_modal", mensaje_error),
    ]

    params += [
        ("ingredientes", ing.strip())
        for ing in ingredientes
        if isinstance(ing, str) and ing.strip()
    ]

    params += [
        ("pasos", paso.strip())
        for paso in pasos
        if isinstance(paso, str) and paso.strip()
    ]

    query_string = urlencode(params)

    return redirect(
        url_for("crear.index") + ("?" + query_string if query_string else "")
    )


# -----------------------------
# VISTA CREAR
# -----------------------------

@crear_bp.route("/crear")
def index():
    form_data = {
        "titulo": request.args.get("titulo", ""),
        "descripcion": request.args.get("descripcion", ""),
        "tiempo": request.args.get("tiempo", ""),
        "raciones": request.args.get("raciones", "4"),
        "categoria": request.args.get("categoria", "Plato Principal"),
        "ingredientes": request.args.getlist("ingredientes"),
        "pasos": request.args.getlist("pasos"),
    }

    error_modal = request.args.get("error_modal", None)

    return render_template(
        "gestionRecetas/crear.html",
        form_data=form_data,
        error_modal=error_modal,
    )


@crear_bp.route("/guardar", methods=["POST"])
def guardar():
    try:
        usuario = obtener_usuario_actual()

        if not usuario:
            flash("Usuario no autenticado.", "error")
            return redirect(url_for("auth.login"))

        nombre = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        tiempo = request.form.get("tiempo", "").strip()
        raciones = request.form.get("raciones", "").strip()
        categoria = request.form.get("categoria", "").strip()

        ingredientes = request.form.getlist("ingredientes[]")
        pasos_texto = request.form.getlist("pasos[]")


        valido, error = validate_form_data(
            nombre,
            descripcion,
            tiempo,
            raciones,
            categoria,
        )

        if not valido:
            return retorno_con_error(
                nombre,
                descripcion,
                tiempo,
                raciones,
                categoria,
                ingredientes,
                pasos_texto,
                error,
            )

        ingredientes_validos = [
            ing.strip()
            for ing in ingredientes
            if ing.strip()
        ]

        if not ingredientes_validos:
            return retorno_con_error(
                nombre,
                descripcion,
                tiempo,
                raciones,
                categoria,
                ingredientes,
                pasos_texto,
                "Debes agregar al menos un ingrediente.",
            )

        if not any(p.strip() for p in pasos_texto):
            return retorno_con_error(
                nombre,
                descripcion,
                tiempo,
                raciones,
                categoria,
                ingredientes,
                pasos_texto,
                "Debes agregar al menos un paso.",
            )

        foto_principal = request.files.get("foto")
        ruta_foto_principal = None
        temp_filename = None

        if foto_principal and foto_principal.filename:
            valido, error = validate_image(
                foto_principal,
                foto_principal.filename,
            )

            if not valido:
                return retorno_con_error(
                    nombre,
                    descripcion,
                    tiempo,
                    raciones,
                    categoria,
                    ingredientes,
                    pasos_texto,
                    error,
                )

            extension = os.path.splitext(
                foto_principal.filename
            )[1]

            temp_filename = f"{uuid.uuid4()}{extension}"

            folder = get_user_folder(usuario.id)

            ruta_foto_principal = save_uploaded_file(
                foto_principal,
                folder,
                temp_filename,
            )

        receta = Receta(
            id_propietario=usuario.id,
            nombre=nombre,
            tipo="normal",
            categoria=categoria,
            descripcion=descripcion,
            tiempo=int(tiempo) if tiempo else 0,
            raciones=raciones,
            foto_principal=ruta_foto_principal,
            creador_original=f"@{usuario.usuario}",
        )

        db.session.add(receta)
        db.session.commit()


        recipe_folder = get_recipe_folder(usuario.id, receta.id)
        ensure_folder_exists(recipe_folder)


        if temp_filename and ruta_foto_principal:
            old_path = os.path.join(
                get_static_root(),
                ruta_foto_principal,
            )

            extension = os.path.splitext(temp_filename)[1]
            new_filename = f"{receta.id}{extension}"

            new_path = os.path.join(
                recipe_folder,
                new_filename,
            )

            os.rename(old_path, new_path)

            ruta_foto_principal = os.path.relpath(
                new_path,
                get_static_root(),
            ).replace("\\", "/")

            receta.foto_principal = ruta_foto_principal
            db.session.commit()

        for ing in ingredientes_validos:
            ingrediente = Ingrediente.query.filter_by(
                nombre=ing
            ).first()

            if not ingrediente:
                ingrediente = Ingrediente(nombre=ing)
                db.session.add(ingrediente)
                db.session.flush()

            relacion = Receta_Ingrediente(
                id_receta=receta.id,
                id_ingrediente=ingrediente.id,
                cantidad="",
                unidad="",
            )

            db.session.add(relacion)

        for i, texto in enumerate(pasos_texto):
            texto = texto.strip()

            if not texto:
                continue

            paso = Paso(
                num_paso=i + 1,
                texto=texto,
                id_receta=receta.id,
            )

            db.session.add(paso)

        db.session.commit()
        flash("¡Receta creada exitosamente!", "success")
        return redirect(url_for("cuenta.index"))

    except Exception as e:
        db.session.rollback()

        return retorno_con_error(
            nombre if "nombre" in locals() else "",
            descripcion if "descripcion" in locals() else "",
            tiempo if "tiempo" in locals() else "",
            raciones if "raciones" in locals() else "",
            categoria if "categoria" in locals() else "",
            ingredientes if "ingredientes" in locals() else [],
            pasos_texto if "pasos_texto" in locals() else [],
            f"Error inesperado: {str(e)}",
        )

@crear_bp.route("/editar/<int:id>", methods=["GET"])
def editar_receta(id):
    """
    Muestra el formulario para editar una receta existente.

    Carga la receta con todas sus versiones para que el usuario
    pueda seleccionar qué versión editar o ver.

    Args:
        id (int): ID de la receta a editar.

    Returns:
        str: Renderizado de la plantilla 'gestionRecetas/editar.html'.
    """
    usuario = obtener_usuario_actual()
    receta = Receta.query.get_or_404(id)

    # Verificar que el usuario sea el propietario
    if receta.id_propietario != usuario.id:
        return redirect(url_for("cuenta.index"))

    # Obtener todas las versiones de esta receta (o sus copias, si es una copia)
    if receta.copia_de:
        # Si es una copia, obtener todas las versiones de la receta original
        versiones = Receta.query.filter_by(id=receta.copia_de).all()
    else:
        # Si es original, obtener todas sus versiones (incluyendo copias)
        versiones = (
            Receta.query.filter((Receta.id == id) | (Receta.copia_de == id))
            .order_by(Receta.version.desc())
            .all()
        )

    # Obtener ingredientes de la receta
    ingredientes = Receta_Ingrediente.query.filter_by(id_receta=id).all()

    # Obtener pasos de la receta con sus fotos (eager loading)
    pasos = Paso.query.filter_by(id_receta=id).order_by(Paso.num_paso).all()
    # Asegurar que las fotos se cargaron (SQLAlchemy lazy loading)
    for paso in pasos:
        _ = paso.fotos  # Fuerza la carga de fotos

    # Verificar si hay error para mostrar modal
    error_modal = request.args.get("error_modal", None)

    return render_template(
        "gestionRecetas/editar.html",
        receta=receta,
        versiones=versiones,
        ingredientes=ingredientes,
        pasos=pasos,
        error_modal=error_modal,
    )


@crear_bp.route("/actualizar", methods=["POST"])
def actualizar():
    """
    Actualiza una receta existente o crea una nueva versión.

    Si es una actualización en la versión actual, se actualiza directamente.
    Si el usuario quiere crear una nueva versión, se incrementa el número de versión.

    Returns:
        Response: Redirección a la página de perfil del usuario o formulario con errores.
    """
    try:
        usuario = obtener_usuario_actual()
        if not usuario:
            flash("Error: Usuario no autenticado.", "error")
            return redirect(url_for("auth.login"))

        receta_id = request.form.get("receta_id", type=int)
        if not receta_id:
            flash("Error: ID de receta inválido.", "error")
            return redirect(url_for("cuenta.perfil"))

        receta = Receta.query.get_or_404(receta_id)

        # Verificar que el usuario sea el propietario
        if receta.id_propietario != usuario.id:
            flash("Error: No tienes permisos para editar esta receta.", "error")
            return redirect(url_for("cuenta.index"))

        # Datos principales
        nombre = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        tiempo = request.form.get("tiempo", "").strip()
        raciones = request.form.get("raciones", "").strip()
        categoria = request.form.get("categoria", "").strip()

        # Validar datos principales
        es_valido, mensaje_error = validate_form_data(
            nombre, descripcion, tiempo, raciones, categoria
        )
        if not es_valido:
            return redirect(
                url_for("crear.editar_receta", id=receta_id, error_modal=mensaje_error)
            )

        # Validar ingredientes
        ingredientes = request.form.getlist("ingredientes[]")
        es_valido, mensaje_error = validate_ingredients(ingredientes)
        if not es_valido:
            return redirect(
                url_for("crear.editar_receta", id=receta_id, error_modal=mensaje_error)
            )

        # Validar pasos
        pasos_texto = request.form.getlist("pasos[]")
        es_valido, mensaje_error = validate_steps(pasos_texto)
        if not es_valido:
            return redirect(
                url_for("crear.editar_receta", id=receta_id, error_modal=mensaje_error)
            )

        # Actualizar datos principales
        receta.nombre = nombre
        receta.descripcion = descripcion
        receta.tiempo = int(tiempo) if tiempo else None
        receta.raciones = raciones
        receta.categoria = categoria

        # Manejar foto principal (upload opcional)
        foto_principal = request.files.get("foto")
        if foto_principal and foto_principal.filename:
            es_valido, mensaje_error = validate_image(
                foto_principal, foto_principal.filename
            )
            if not es_valido:
                return redirect(
                    url_for(
                        "crear.editar_receta", id=receta_id, error_modal=mensaje_error
                    )
                )

            extension = os.path.splitext(foto_principal.filename)[1]
            folder = get_recipe_folder(usuario.id, receta.id)
            ensure_folder_exists(folder)
            filename = f"{receta.id}{extension}"
            ruta_foto = save_uploaded_file(foto_principal, folder, filename)
            receta.foto_principal = ruta_foto

        # Incrementar versión si hay cambios significativos
        receta.version += 1

        # Actualizar ingredientes (eliminar y recrear)
        try:
            Receta_Ingrediente.query.filter_by(id_receta=receta.id).delete()
            ingredientes_limpios = [ing.strip() for ing in ingredientes if ing.strip()]

            for ing in ingredientes_limpios:
                ingrediente = Ingrediente.query.filter_by(nombre=ing).first()
                if not ingrediente:
                    ingrediente = Ingrediente(nombre=ing)
                    db.session.add(ingrediente)
                    db.session.flush()

                rel = Receta_Ingrediente(
                    id_receta=receta.id,
                    id_ingrediente=ingrediente.id,
                    cantidad="",
                    unidad="",
                )
                db.session.add(rel)
        except Exception as e:
            db.session.rollback()
            return redirect(
                url_for(
                    "crear.editar_receta",
                    id=receta_id,
                    error_modal=f"Error al actualizar ingredientes: {str(e)}",
                )
            )

        # Actualizar pasos
        try:
            # ANTES DE BORRAR: eliminar fotos del disco de los pasos antiguos
            pasos_antiguos = Paso.query.filter_by(id_receta=receta.id).all()
            for paso_antiguo in pasos_antiguos:
                for foto in paso_antiguo.fotos:
                    # Borrar archivo del disco
                    ruta_disco = os.path.join(get_static_root(), foto.foto)
                    if os.path.exists(ruta_disco):
                        try:
                            os.remove(ruta_disco)
                        except Exception:
                            pass  # Continuar aunque falle

            # Borrar pasos (cascada borra Fotos de BD automáticamente)
            Paso.query.filter_by(id_receta=receta.id).delete()

            pasos_limpios = [paso.strip() for paso in pasos_texto if paso.strip()]
            fotos_pasos = request.files.getlist("fotos_pasos[]")

            for i, texto in enumerate(pasos_limpios):
                paso = Paso(num_paso=i + 1, texto=texto, id_receta=receta.id)
                db.session.add(paso)
                db.session.flush()

                # Imagen del paso
                if i < len(fotos_pasos):
                    foto_archivo = fotos_pasos[i]
                    if foto_archivo and foto_archivo.filename:
                        es_valido, mensaje_error = validate_image(
                            foto_archivo, foto_archivo.filename
                        )
                        if not es_valido:
                            return redirect(
                                url_for(
                                    "crear.editar_receta",
                                    id=receta_id,
                                    error_modal=f"Error en imagen del paso {i+1}: {mensaje_error}",
                                )
                            )

                        extension = os.path.splitext(foto_archivo.filename)[1]
                        filename = f"paso{paso.num_paso}{extension}"
                        folder = get_steps_folder(usuario.id, receta.id)
                        ensure_folder_exists(folder)
                        ruta_foto = save_uploaded_file(foto_archivo, folder, filename)

                        foto = Foto(foto=ruta_foto, id_paso=paso.id)
                        db.session.add(foto)
        except Exception as e:
            db.session.rollback()
            return redirect(
                url_for(
                    "crear.editar_receta",
                    id=receta_id,
                    error_modal=f"Error al actualizar pasos: {str(e)}",
                )
            )

        db.session.commit()
        flash("¡Receta actualizada exitosamente!", "success")
        return redirect(url_for("cuenta.perfil"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error inesperado al actualizar la receta: {str(e)}", "error")
        return redirect(url_for("cuenta.perfil"))
