from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models.receta import Receta
from models.usuario import Usuario
from models.receta_usuario_likes import Receta_Usuario_Likes
from models.seguidor import Seguidor
from models.amigo import Amigo
from models.solicitud_amistad import SolicitudAmistad
from services import (
    obtener_usuario_actual,
    load_smtp_settings,
    save_smtp_settings,
    hash_password,
    is_smtp_configured,
)
from database import db
import os
import shutil
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import uuid
from utils.data_utils import (
    get_profile_photo_folder,
    save_uploaded_file,
    get_static_root,
    get_recipe_folder,
)

# Blueprint de la sección "cuenta"
cuenta_bp = Blueprint("cuenta", __name__)


@cuenta_bp.route("/")
def index():
    """
    Muestra la página principal con todas las recetas disponibles.

    Returns:
        Response: Plantilla HTML con la lista de recetas, incluyendo
        autor, número de favoritos y si el usuario actual la ha marcado
        como favorita.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        if "usuario_id" in session:
            session.clear()
        return redirect(url_for("auth.login"))

    recetas = Receta.query.filter(Receta.id_propietario != usuario.id).all()
    # --- Optimización: resolver autores, likes y favoritos en 3 queries planas ---
    # 1. IDs de recetas que el usuario actual tiene como favoritas
    ids_recetas = [r.id for r in recetas]
    favoritos_ids = {
        row.id_receta
        for row in Receta_Usuario_Likes.query.filter(
            Receta_Usuario_Likes.id_receta.in_(ids_recetas),
            Receta_Usuario_Likes.id_usuario == usuario.id,
        ).all()
    }

    # 2. Conteo de likes agrupado por receta
    from sqlalchemy import func
    likes_rows = (
        db.session.query(
            Receta_Usuario_Likes.id_receta,
            func.count(Receta_Usuario_Likes.id_usuario).label("total"),
        )
        .filter(Receta_Usuario_Likes.id_receta.in_(ids_recetas))
        .group_by(Receta_Usuario_Likes.id_receta)
        .all()
    )
    likes_map = {row.id_receta: row.total for row in likes_rows}

    # 3. Autores en una sola query
    ids_propietarios = {r.id_propietario for r in recetas}
    autores_map = {
        u.id: u
        for u in Usuario.query.filter(Usuario.id.in_(ids_propietarios)).all()
    }

    recetas_data = []
    for r in recetas:
        autor = autores_map.get(r.id_propietario)
        nombre_autor = (
            f"{autor.nombre} {autor.apellidos}" if autor else "Desconocido"
        )
        recetas_data.append(
            {
                "id": r.id,
                "nombre": r.nombre,
                "categoria": r.categoria,
                "descripcion": r.descripcion,
                "tiempo": r.tiempo,
                "raciones": r.raciones,
                "foto": r.foto_principal,
                "autor": nombre_autor,
                "likes": likes_map.get(r.id, 0),
                "favorito": r.id in favoritos_ids,
            }
        )

    return render_template("cuenta/index.html", recetas=recetas_data)


@cuenta_bp.route("/receta/<int:id>")
def ver_receta(id):
    """
    Muestra la información completa de una receta específica.

    Args:
        id (int): ID de la receta.

    Returns:
        Response: Plantilla HTML con los detalles de la receta.
    """
    receta = Receta.query.get_or_404(id)
    autor = Usuario.query.get(receta.id_propietario)
    return render_template("cuenta/receta.html", receta=receta, autor=autor)


@cuenta_bp.route("/perfil")
def perfil():
    """
    Muestra el perfil del usuario logueado junto con sus recetas creadas.

    Returns:
        Response: Plantilla HTML con los datos del usuario y sus recetas.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    from models.seguidor import Seguidor

    recetas = Receta.query.filter_by(id_propietario=usuario.id).all()
    recetas_data = []

    total_likes = 0
    for r in recetas:
        likes = Receta_Usuario_Likes.query.filter_by(id_receta=r.id).count()
        total_likes += likes

        recetas_data.append(
            {
                "id": r.id,
                "nombre": r.nombre,
                "categoria": r.categoria,
                "descripcion": r.descripcion,
                "tiempo": r.tiempo,
                "raciones": r.raciones,
                "foto": r.foto_principal,
                "likes": likes,
            }
        )

    # Calcular seguidores y seguidos
    seguidores_count = Seguidor.query.filter_by(id_seguido=usuario.id).count()
    seguidos_count = Seguidor.query.filter_by(id_seguidor=usuario.id).count()

    # Obtener recetas que le han gustado (likes)
    likes_rel = Receta_Usuario_Likes.query.filter_by(id_usuario=usuario.id).all()
    recetas_likes_data = []

    for rel in likes_rel:
        receta = Receta.query.get(rel.id_receta)
        autor = Usuario.query.get(receta.id_propietario)

        recetas_likes_data.append(
            {
                "id": receta.id,
                "nombre": receta.nombre,
                "categoria": receta.categoria,
                "descripcion": receta.descripcion,
                "tiempo": receta.tiempo,
                "raciones": receta.raciones,
                "foto": receta.foto_principal,
                "autor": (
                    f"{autor.nombre} {autor.apellidos}" if autor else "Desconocido"
                ),
            }
        )

    # Obtener usuarios que sigue
    seguidos_rel = Seguidor.query.filter_by(id_seguidor=usuario.id).all()
    usuarios_seguidos_data = []

    for rel in seguidos_rel:
        usuario_seguido = Usuario.query.get(rel.id_seguido)
        if usuario_seguido:
            usuarios_seguidos_data.append(usuario_seguido)

    return render_template(
        "cuenta/perfil.html",
        usuario=usuario,
        recetas=recetas_data,
        recetas_likes=recetas_likes_data,
        usuarios_seguidos=usuarios_seguidos_data,
        total_likes=total_likes,
        seguidores=seguidores_count,
        seguidos=seguidos_count,
    )


@cuenta_bp.route("/subir_foto_perfil", methods=["POST"])
def subir_foto_perfil():
    """
    Sube una foto de perfil para el usuario actual.

    Returns:
        Response: Redirección al perfil.
    """
    usuario = obtener_usuario_actual()
    if not usuario:
        return redirect(url_for("auth.login"))

    foto = request.files.get("foto_perfil")
    ALLOWED = {"jpg", "jpeg", "png", "gif"}
    MAX_SIZE = 5 * 1024 * 1024  # 5 MB

    if foto and foto.filename:
        ext = os.path.splitext(foto.filename)[1].lstrip(".")
        if ext.lower() not in ALLOWED:
            flash("Tipo de archivo no permitido. Solo JPG, PNG y GIF.", "danger")
            return redirect(url_for("cuenta.perfil"))

        foto.seek(0, os.SEEK_END)
        size = foto.tell()
        foto.seek(0)
        if size > MAX_SIZE:
            flash("La imagen no puede superar 5 MB.", "danger")
            return redirect(url_for("cuenta.perfil"))

        filename = f"{uuid.uuid4()}.{ext.lower()}"
        folder = get_profile_photo_folder(usuario.id)
        ruta_foto = save_uploaded_file(foto, folder, filename)

        usuario.foto = ruta_foto
        db.session.commit()

    return redirect(url_for("cuenta.perfil"))


@cuenta_bp.route("/favorito/<int:id_receta>")
def toggle_favorito(id_receta):
    """
    Añade o elimina una receta de los favoritos del usuario.

    Args:
        id_receta (int): ID de la receta.

    Returns:
        Response: Redirección a la página anterior o al índice.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    # C4: verificar que la receta exista
    receta = Receta.query.get(id_receta)
    if not receta:
        flash("Receta no encontrada.", "danger")
        return redirect(url_for("cuenta.index"))

    # Buscar si ya existe la relación de favorito
    favorito = Receta_Usuario_Likes.query.filter_by(
        id_receta=id_receta, id_usuario=usuario.id
    ).first()

    if favorito:
        db.session.delete(favorito)
    else:
        nuevo = Receta_Usuario_Likes(id_receta=id_receta, id_usuario=usuario.id)
        db.session.add(nuevo)

    db.session.commit()

    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/amigos")
def amigos():
    """
    Muestra solicitudes de amistad pendientes y lista de amigos actuales.

    Returns:
        Response: Plantilla HTML con solicitudes y amigos.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    # Obtener solicitudes recibidas (pendientes)
    solicitudes_recibidas = SolicitudAmistad.query.filter_by(
        id_receptor=usuario.id
    ).all()
    solicitudes_data = []

    for solicitud in solicitudes_recibidas:
        remitente = Usuario.query.get(solicitud.id_remitente)
        if remitente:
            solicitudes_data.append({"id": solicitud.id, "usuario": remitente})

    # Obtener amigos actuales (evitar duplicados)
    amigos_rel = Amigo.query.filter(
        ((Amigo.id_usuario == usuario.id) & (Amigo.aceptado == True))
        | ((Amigo.id_amigo == usuario.id) & (Amigo.aceptado == True))
    ).all()

    amigos_dict = {}  # Usar diccionario para evitar duplicados
    for amigo_rel in amigos_rel:
        if amigo_rel.id_usuario == usuario.id:
            amigo_usuario = Usuario.query.get(amigo_rel.id_amigo)
            amigo_id = amigo_rel.id_amigo
        else:
            amigo_usuario = Usuario.query.get(amigo_rel.id_usuario)
            amigo_id = amigo_rel.id_usuario

        if amigo_usuario and amigo_id not in amigos_dict:
            amigos_dict[amigo_id] = amigo_usuario

    amigos_data = list(amigos_dict.values())

    return render_template(
        "cuenta/amigos.html", solicitudes=solicitudes_data, amigos=amigos_data
    )


@cuenta_bp.route("/favoritos")
def favoritos():
    """Redirige a la página de amigos por compatibilidad."""
    return redirect(url_for("cuenta.amigos"))


@cuenta_bp.route("/borrar_receta/<int:id_receta>", methods=["POST"])
def borrar_receta(id_receta):
    """
    Elimina una receta y sus archivos asociados.

    Verifica que el usuario actual sea el propietario de la receta antes de
    eliminarla. Borra las fotos de la receta y pasos del disco duro.

    Args:
        id_receta (int): ID de la receta a eliminar.

    Returns:
        Response: Redirección al perfil del usuario o error 403 si no autorizado.
    """
    usuario = obtener_usuario_actual()

    # C3: proteger antes de usar usuario.id
    if not usuario:
        return redirect(url_for("auth.login"))

    receta = Receta.query.get_or_404(id_receta)

    # Seguridad: solo el dueño puede borrar
    if receta.id_propietario != usuario.id:
        return "No autorizado", 403

    # Borrar foto principal del disco
    if receta.foto_principal:
        ruta = os.path.join(get_static_root(), receta.foto_principal)
        if os.path.exists(ruta):
            os.remove(ruta)

    # Borrar la carpeta de la receta completa con pasos/fotos
    receta_folder = get_recipe_folder(usuario.id, receta.id)
    if os.path.exists(receta_folder):
        shutil.rmtree(receta_folder)

    # Borrar receta de la BD (cascade elimina pasos y fotos)
    db.session.delete(receta)
    db.session.commit()

    return redirect(url_for("cuenta.perfil"))


@cuenta_bp.route("/seguir/<int:id_usuario>", methods=["POST"])
def seguir(id_usuario):
    """
    Permite al usuario seguir a otro usuario.

    Args:
        id_usuario (int): ID del usuario a seguir.

    Returns:
        Response: Redirección a la página anterior o al índice.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    if id_usuario == usuario.id:
        flash("No puedes seguirte a ti mismo.", "error")
        return redirect(request.referrer or url_for("cuenta.index"))

    existente = Seguidor.query.filter_by(
        id_seguidor=usuario.id, id_seguido=id_usuario
    ).first()

    if existente:
        flash("Ya sigues a este usuario.", "info")
    else:
        nuevo = Seguidor(id_seguidor=usuario.id, id_seguido=id_usuario)
        db.session.add(nuevo)
        db.session.commit()
        flash("Ahora sigues a este usuario.", "success")

    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/dejar_seguir/<int:id_usuario>", methods=["POST"])
def dejar_seguir(id_usuario):
    """
    Permite al usuario dejar de seguir a otro usuario.

    Args:
        id_usuario (int): ID del usuario a dejar de seguir.

    Returns:
        Response: Redirección a la página anterior o al índice.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    existente = Seguidor.query.filter_by(
        id_seguidor=usuario.id, id_seguido=id_usuario
    ).first()

    if existente:
        db.session.delete(existente)
        db.session.commit()
        flash("Has dejado de seguir a este usuario.", "success")
    else:
        flash("No sigues a este usuario.", "info")

    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/usuario/<int:id_usuario>")
def perfil_usuario(id_usuario):
    """
    Muestra el perfil de otro usuario.

    Args:
        id_usuario (int): ID del usuario a mostrar.

    Returns:
        Response: Plantilla HTML con el perfil del usuario.
    """
    usuario_actual = obtener_usuario_actual()
    usuario = Usuario.query.get_or_404(id_usuario)

    if not usuario_actual:
        return redirect(url_for("auth.login"))

    # Si es el mismo usuario, redirigir al perfil personal
    if usuario.id == usuario_actual.id:
        return redirect(url_for("cuenta.perfil"))

    # Obtener recetas del usuario
    recetas = Receta.query.filter_by(id_propietario=usuario.id).all()
    recetas_data = []

    total_likes = 0
    for r in recetas:
        likes = Receta_Usuario_Likes.query.filter_by(id_receta=r.id).count()
        total_likes += likes

        recetas_data.append(
            {
                "id": r.id,
                "nombre": r.nombre,
                "categoria": r.categoria,
                "descripcion": r.descripcion,
                "tiempo": r.tiempo,
                "raciones": r.raciones,
                "foto": r.foto_principal,
                "likes": likes,
            }
        )

    # Calcular seguidores y seguidos
    seguidores_count = Seguidor.query.filter_by(id_seguido=usuario.id).count()
    seguidos_count = Seguidor.query.filter_by(id_seguidor=usuario.id).count()

    # Verificar si el usuario actual sigue a este usuario
    sigo_usuario = (
        Seguidor.query.filter_by(
            id_seguidor=usuario_actual.id, id_seguido=usuario.id
        ).first()
        is not None
    )

    # Verificar si el usuario actual es amigo de este usuario
    amigo = Amigo.query.filter(
        ((Amigo.id_usuario == usuario_actual.id) & (Amigo.id_amigo == usuario.id))
        | ((Amigo.id_usuario == usuario.id) & (Amigo.id_amigo == usuario_actual.id))
    ).first()

    # Verificar si hay solicitud de amistad pendiente
    solicitud_pendiente = SolicitudAmistad.query.filter(
        (
            (SolicitudAmistad.id_remitente == usuario_actual.id)
            & (SolicitudAmistad.id_receptor == usuario.id)
        )
        | (
            (SolicitudAmistad.id_remitente == usuario.id)
            & (SolicitudAmistad.id_receptor == usuario_actual.id)
        )
    ).first()

    return render_template(
        "cuenta/usuario.html",
        usuario=usuario,
        recetas=recetas_data,
        total_likes=total_likes,
        seguidores=seguidores_count,
        seguidos=seguidos_count,
        sigo=sigo_usuario,
        es_amigo=amigo and amigo.aceptado if amigo else False,
        solicitud_pendiente=solicitud_pendiente,
        usuario_actual=usuario_actual,
    )


@cuenta_bp.route("/solicitar_amistad/<int:id_usuario>", methods=["POST"])
def solicitar_amistad(id_usuario):
    """
    Envía una solicitud de amistad a otro usuario.

    Args:
        id_usuario (int): ID del usuario al que se le envía la solicitud.

    Returns:
        Response: Redirección a la página anterior.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    if id_usuario == usuario.id:
        flash("No puedes enviar una solicitud de amistad a ti mismo.", "error")
        return redirect(request.referrer or url_for("cuenta.index"))

    # Verificar si ya existe una solicitud
    solicitud_existente = SolicitudAmistad.query.filter(
        (
            (SolicitudAmistad.id_remitente == usuario.id)
            & (SolicitudAmistad.id_receptor == id_usuario)
        )
        | (
            (SolicitudAmistad.id_remitente == id_usuario)
            & (SolicitudAmistad.id_receptor == usuario.id)
        )
    ).first()

    if solicitud_existente:
        flash("Ya existe una solicitud de amistad con este usuario.", "info")
        return redirect(request.referrer or url_for("cuenta.index"))

    # Verificar si ya son amigos
    amigo_existente = Amigo.query.filter(
        ((Amigo.id_usuario == usuario.id) & (Amigo.id_amigo == id_usuario))
        | ((Amigo.id_usuario == id_usuario) & (Amigo.id_amigo == usuario.id))
    ).first()

    if amigo_existente:
        flash("Ya sois amigos.", "info")
        return redirect(request.referrer or url_for("cuenta.index"))

    # Crear nueva solicitud
    nueva_solicitud = SolicitudAmistad(id_remitente=usuario.id, id_receptor=id_usuario)
    db.session.add(nueva_solicitud)
    db.session.commit()

    flash("Solicitud de amistad enviada.", "success")
    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/aceptar_amistad/<int:id_solicitud>", methods=["POST"])
def aceptar_amistad(id_solicitud):
    """
    Acepta una solicitud de amistad.

    Args:
        id_solicitud (int): ID de la solicitud a aceptar.

    Returns:
        Response: Redirección a la página anterior.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    solicitud = SolicitudAmistad.query.get_or_404(id_solicitud)

    # Verificar que el usuario actual es el receptor
    if solicitud.id_receptor != usuario.id:
        flash("No tienes permiso para aceptar esta solicitud.", "error")
        return redirect(request.referrer or url_for("cuenta.index"))

    # Crear la amistad (bidireccional)
    amigo1 = Amigo(
        id_usuario=solicitud.id_remitente, id_amigo=solicitud.id_receptor, aceptado=True
    )
    amigo2 = Amigo(
        id_usuario=solicitud.id_receptor, id_amigo=solicitud.id_remitente, aceptado=True
    )

    db.session.add(amigo1)
    db.session.add(amigo2)
    db.session.delete(solicitud)
    db.session.commit()

    flash("Solicitud de amistad aceptada.", "success")
    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/rechazar_amistad/<int:id_solicitud>", methods=["POST"])
def rechazar_amistad(id_solicitud):
    """
    Rechaza una solicitud de amistad.

    Args:
        id_solicitud (int): ID de la solicitud a rechazar.

    Returns:
        Response: Redirección a la página anterior.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    solicitud = SolicitudAmistad.query.get_or_404(id_solicitud)

    # Verificar que el usuario actual es el receptor
    if solicitud.id_receptor != usuario.id:
        flash("No tienes permiso para rechazar esta solicitud.", "error")
        return redirect(request.referrer or url_for("cuenta.index"))

    db.session.delete(solicitud)
    db.session.commit()

    flash("Solicitud de amistad rechazada.", "success")
    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/eliminar_amigo/<int:id_amigo>", methods=["POST"])
def eliminar_amigo(id_amigo):
    """
    Elimina una amistad existente.

    Args:
        id_amigo (int): ID del amigo a eliminar.

    Returns:
        Response: Redirección a la página anterior.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    # Buscar y eliminar ambas direcciones de amistad
    amigo1 = Amigo.query.filter_by(id_usuario=usuario.id, id_amigo=id_amigo).first()
    amigo2 = Amigo.query.filter_by(id_usuario=id_amigo, id_amigo=usuario.id).first()

    if amigo1:
        db.session.delete(amigo1)
    if amigo2:
        db.session.delete(amigo2)

    db.session.commit()

    flash("Se eliminó la amistad.", "success")
    return redirect(request.referrer or url_for("cuenta.index"))


@cuenta_bp.route("/editar_perfil")
def editar_perfil():
    """
    Muestra la página para editar el perfil del usuario.

    Returns:
        Response: Plantilla HTML con formulario de edición de perfil.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    return render_template("cuenta/editar_perfil.html", usuario=usuario)


@cuenta_bp.route("/actualizar_perfil", methods=["POST"])
def actualizar_perfil():
    """
    Actualiza los datos del perfil del usuario.

    Returns:
        Response: Redirección al perfil o página de edición si hay error.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    nombre = request.form.get("nombre", "").strip()
    apellidos = request.form.get("apellidos", "").strip()
    usuario_username = request.form.get("usuario", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    contrasena_actual = request.form.get("contrasena_actual", "").strip()
    contrasena_nueva = request.form.get("contrasena_nueva", "").strip()
    contrasena_confirmar = request.form.get("contrasena_confirmar", "").strip()

    # Validaciones básicas
    if not nombre or not apellidos or not usuario_username:
        flash("Por favor completa los campos requeridos", "error")
        return redirect(url_for("cuenta.editar_perfil"))

    # Verificar que el nuevo usuario no esté en uso por otro usuario
    usuario_existente = Usuario.query.filter(
        Usuario.usuario == usuario_username, Usuario.id != usuario.id
    ).first()
    if usuario_existente:
        flash("Este nombre de usuario ya está en uso", "error")
        return redirect(url_for("cuenta.editar_perfil"))

    # Validar cambio de contraseña
    if contrasena_nueva or contrasena_actual or contrasena_confirmar:
        # Si quiere cambiar contraseña, todos los campos son obligatorios
        if not contrasena_actual or not contrasena_nueva or not contrasena_confirmar:
            flash("Completa todos los campos de contraseña", "error")
            return redirect(url_for("cuenta.editar_perfil"))

        # Verificar que la contraseña actual sea correcta
        if not check_password_hash(usuario.contrasena, contrasena_actual):
            flash("La contraseña actual es incorrecta", "error")
            return redirect(url_for("cuenta.editar_perfil"))

        # Verificar que las nuevas contraseñas coincidan
        if contrasena_nueva != contrasena_confirmar:
            flash("Las nuevas contraseñas no coinciden", "error")
            return redirect(url_for("cuenta.editar_perfil"))

        # Verificar que la nueva contraseña sea diferente
        if contrasena_nueva == contrasena_actual:
            flash("La nueva contraseña debe ser diferente", "error")
            return redirect(url_for("cuenta.editar_perfil"))

    # Actualizar datos básicos
    usuario.nombre = nombre
    usuario.apellidos = apellidos
    usuario.usuario = usuario_username
    usuario.descripcion = descripcion

    # Actualizar contraseña si se proporciona y validó correctamente
    if contrasena_nueva:
        usuario.contrasena = hash_password(contrasena_nueva)
        flash("Contraseña actualizada correctamente", "success")

    db.session.commit()
    flash("Perfil actualizado correctamente", "success")

    return redirect(url_for("cuenta.perfil"))


@cuenta_bp.route("/configurar_smtp", methods=["GET", "POST"])
def configurar_smtp():
    """
    Muestra y guarda la configuración SMTP para el envío de correos.

    Returns:
        Response: Formulario de configuración SMTP.
    """
    usuario = obtener_usuario_actual()
    if not usuario:
        return redirect(url_for("auth.login"))

    smtp_config = load_smtp_settings()

    if request.method == "POST":
        datos = {
            "host": request.form.get("host", "").strip(),
            "port": request.form.get("port", "").strip(),
            "user": request.form.get("user", "").strip(),
            "password": request.form.get("password", "").strip(),
            "from_address": request.form.get("from_address", "").strip(),
            "use_tls": request.form.get("use_tls") == "on",
            "use_ssl": request.form.get("use_ssl") == "on",
        }

        if (
            not datos["host"]
            or not datos["port"]
            or not datos["user"]
            or not datos["password"]
            or not datos["from_address"]
        ):
            flash("Completa todos los campos de SMTP", "danger")
            return redirect(url_for("cuenta.configurar_smtp"))

        try:
            int(datos["port"])
        except ValueError:
            flash("Puerto SMTP inválido", "danger")
            return redirect(url_for("cuenta.configurar_smtp"))

        save_smtp_settings(datos)
        flash("Configuración SMTP guardada correctamente", "success")
        return redirect(url_for("cuenta.ajustes"))

    return render_template(
        "cuenta/configurar_smtp.html",
        smtp=smtp_config,
        smtp_enabled=is_smtp_configured(),
    )


@cuenta_bp.route("/ajustes")
def ajustes():
    """
    Muestra la página de ajustes del usuario.

    Returns:
        Response: Plantilla HTML con opciones de ajustes.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    return render_template("cuenta/ajustes.html", usuario=usuario)


@cuenta_bp.route("/busqueda")
def busqueda():
    """
    Muestra la página de búsqueda con las primeras recetas.

    Returns:
        Response: Plantilla HTML con grid inicial de recetas.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    # Cargar primeras 20 recetas, ordenadas por id descendente (más nuevas primero)
    recetas = Receta.query.order_by(Receta.id.desc()).limit(20).all()
    recetas_data = []

    for r in recetas:
        autor = Usuario.query.get(r.id_propietario)
        likes = Receta_Usuario_Likes.query.filter_by(id_receta=r.id).count()
        es_favorito = (
            Receta_Usuario_Likes.query.filter_by(
                id_receta=r.id, id_usuario=usuario.id
            ).first()
            is not None
        )

        foto_path = r.foto_principal

        recetas_data.append(
            {
                "id": r.id,
                "titulo": r.nombre,
                "descripcion": r.descripcion,
                "autor": autor.nombre if autor else "Desconocido",
                "likes": likes,
                "es_favorito": es_favorito,
                "foto": foto_path,
            }
        )

    return render_template(
        "cuenta/busqueda.html", usuario=usuario, recetas=recetas_data
    )


@cuenta_bp.route("/api/busqueda")
def api_busqueda():
    """
    API para buscar y cargar más recetas.

    Query params: q (término de búsqueda), page, limit
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return {"error": "No autorizado"}, 401

    query_text = request.args.get("q", "").strip()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    offset = (page - 1) * limit

    # Construir query base
    query = Receta.query

    # Filtrar si hay término de búsqueda
    if query_text:
        search_term = f"%{query_text}%"
        query = query.filter(
            (Receta.nombre.ilike(search_term)) |
            (Receta.descripcion.ilike(search_term)) |
            (Receta.categoria.ilike(search_term))
        )

    recetas = query.order_by(Receta.id.desc()).offset(offset).limit(limit).all()
    recetas_data = []

    for r in recetas:
        autor = Usuario.query.get(r.id_propietario)
        likes = Receta_Usuario_Likes.query.filter_by(id_receta=r.id).count()
        es_favorito = (
            Receta_Usuario_Likes.query.filter_by(
                id_receta=r.id, id_usuario=usuario.id
            ).first()
            is not None
        )

        foto_path = r.foto_principal

        recetas_data.append(
            {
                "id": r.id,
                "titulo": r.nombre,
                "descripcion": r.descripcion,
                "autor": autor.nombre if autor else "Desconocido",
                "likes": likes,
                "es_favorito": es_favorito,
                "foto": foto_path,
            }
        )

    return {"recetas": recetas_data}


@cuenta_bp.route("/privacidad")
def privacidad():
    """
    Muestra la página de configuración de privacidad.

    Returns:
        Response: Plantilla HTML con opciones de privacidad.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    return render_template("cuenta/privacidad.html", usuario=usuario)


@cuenta_bp.route("/alertas")
def alertas():
    """
    Muestra la página de configuración de alertas.

    Returns:
        Response: Plantilla HTML con opciones de alertas.
    """
    usuario = obtener_usuario_actual()

    if not usuario:
        return redirect(url_for("auth.login"))

    return render_template("cuenta/alertas.html", usuario=usuario)
