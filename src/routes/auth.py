from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services import (
    login_usuario,
    logout_usuario,
    crear_usuario,
    verificar_disponibilidad,
    esta_autenticado,
    hash_password,
    send_email,
    is_smtp_configured,
    obtener_usuario_actual,
)
from models.usuario import Usuario
from database import db
import random
import string

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Gestiona el inicio de sesión de usuarios.

    Flujo:
        - GET: Muestra el formulario de login.
        - POST: Procesa las credenciales introducidas por el usuario.

    Returns:
        Response: Renderiza la página de login o redirige al área de usuario si las credenciales son válidas.
    """

    # Solo redirigir a /index si el usuario está autenticado Y existe en BD
    if esta_autenticado() and obtener_usuario_actual():
        return redirect(url_for("cuenta.index"))

    # Si hay una sesión corrupta (usuario_id pero sin usuario en BD), limpiarla
    if "usuario_id" in session and not obtener_usuario_actual():
        session.clear()

    if request.method == "POST":
        # Datos del formulario HTML
        user_input = request.form.get("nombre_usuario")
        pass_input = request.form.get("contraseña")

        result = login_usuario(user_input, pass_input)

        if result["usuario"]:
            flash(f"Bienvenido de nuevo, {result['usuario'].nombre}", "success")
            return redirect(url_for("cuenta.index"))

        flash(result["error"], "danger")

    return render_template("usuario/login.html")


@auth_bp.route("/logout")
def logout():
    """
    Cierra la sesión del usuario actual.

    Elimina la sesión activa y redirige al usuario a la página de login.

    Returns:
        Response: Redirección a la página de inicio de sesión.
    """
    logout_usuario()
    return redirect(url_for(".login"))


@auth_bp.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    """
    Gestiona el registro de nuevos usuarios.

    Flujo:
        - GET: Muestra el formulario de registro.
        - POST: Valida los datos introducidos y crea un nuevo usuario.

    Validaciones:
        - Comprueba que las contraseñas coincidan antes de crear el usuario.

    Returns:
        Response: Renderiza el formulario o redirige al login tras registro exitoso.
    """

    if esta_autenticado():
        return redirect(url_for("cuenta.index"))

    if request.method == "POST":
        # Verificar si las contraseñas coinciden antes de ir al servicio
        pass1 = request.form.get("contrasena")
        pass2 = request.form.get("contrarep")

        if pass1 != pass2:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for(".registrarse"))

        # Verificar disponibilidad de usuario y gmail
        usuario_input = request.form.get("usuario")
        gmail_input = request.form.get("gmail")
        disponible, mensaje = verificar_disponibilidad(usuario_input, gmail_input)
        if not disponible:
            flash(mensaje, "danger")
            return redirect(url_for(".registrarse"))

        # Mapeo de datos para el servicio crear_usuario
        datos = {
            "nombre": request.form.get("nombre"),
            "apellidos": request.form.get("apellidos"),
            "usuario": usuario_input,
            "contrasena": pass1,
            "gmail": gmail_input,
        }

        exito, mensaje = crear_usuario(datos)

        if exito:
            flash("¡Cuenta creada! Ahora puedes iniciar sesión.", "success")
            return redirect(url_for(".login"))
        else:
            flash(mensaje, "danger")

    return render_template("usuario/registrarse.html")


@auth_bp.route("/recuperar_contraseña", methods=["GET", "POST"])
def recuperar_contraseña():
    """
    Primer paso: solicita el email del usuario para recuperar contraseña.
    Genera un código de verificación y lo almacena en sesión.

    Returns:
        Response: Formulario o redirección a verificar código.
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        # Verificar que el email existe
        usuario = Usuario.query.filter_by(gmail=email).first()
        if not usuario:
            flash("No existe cuenta con este email", "danger")
            return redirect(url_for("auth.recuperar_contraseña"))

        # Generar código de 6 dígitos
        codigo = "".join(random.choices(string.digits, k=6))

        # Guardar en sesión
        session["recovery_email"] = email
        session["recovery_codigo"] = codigo
        session["recovery_user_id"] = usuario.id

        # Intentar enviar el código por SMTP
        if is_smtp_configured():
            asunto = "Código de verificación para recuperar tu contraseña"
            cuerpo = f"Tu código de verificación es: {codigo}\n\nSi no solicitaste este correo, ignóralo."
            html_cuerpo = f"<p>Tu código de verificación es: <strong>{codigo}</strong></p><p>Si no solicitaste este correo, ignóralo.</p>"
            exito, mensaje_email = send_email(email, asunto, cuerpo, html_cuerpo)
            if exito:
                flash(
                    "Código de verificación enviado por email. Revisa tu bandeja de entrada.",
                    "success",
                )
            else:
                flash(f"No se pudo enviar el email: {mensaje_email}", "warning")
                flash(f"Código de verificación (temporal): {codigo}", "info")
        else:
            flash(
                "SMTP no está configurado. El código se muestra en pantalla para pruebas.",
                "warning",
            )
            flash(f"Código de verificación (simulado): {codigo}", "info")

        return redirect(url_for("auth.verificar_codigo"))

    return render_template("usuario/recuperar_contraseña.html")


@auth_bp.route("/verificar_codigo", methods=["GET", "POST"])
def verificar_codigo():
    """
    Segundo paso: verifica el código enviado.

    Returns:
        Response: Formulario de verificación o redirección a nueva contraseña.
    """
    if "recovery_email" not in session:
        flash("Primero debes solicitar recuperación de contraseña", "danger")
        return redirect(url_for("auth.recuperar_contraseña"))

    if request.method == "POST":
        codigo_ingresado = request.form.get("codigo", "").strip()
        codigo_correcto = session.get("recovery_codigo")

        if codigo_ingresado != codigo_correcto:
            flash("Código incorrecto", "danger")
            return redirect(url_for("auth.verificar_codigo"))

        # Código verificado
        session["codigo_verificado"] = True
        flash("Código verificado correctamente", "success")
        return redirect(url_for("auth.nueva_contraseña"))

    email = session.get("recovery_email", "")
    return render_template("usuario/verificar_codigo.html", email=email)


@auth_bp.route("/nueva_contraseña", methods=["GET", "POST"])
def nueva_contraseña():
    """
    Tercer paso: establece la nueva contraseña.

    Returns:
        Response: Formulario o redirección a login.
    """
    if not session.get("codigo_verificado"):
        flash("Debes verificar el código primero", "danger")
        return redirect(url_for("auth.recuperar_contraseña"))

    if request.method == "POST":
        contrasena_nueva = request.form.get("contrasena_nueva", "").strip()
        contrasena_confirmar = request.form.get("contrasena_confirmar", "").strip()

        if not contrasena_nueva or not contrasena_confirmar:
            flash("Completa todos los campos", "danger")
            return redirect(url_for("auth.nueva_contraseña"))

        if contrasena_nueva != contrasena_confirmar:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for("auth.nueva_contraseña"))

        if len(contrasena_nueva) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
            return redirect(url_for("auth.nueva_contraseña"))

        # Actualizar contraseña en BD
        user_id = session.get("recovery_user_id")
        usuario = Usuario.query.get(user_id)

        if usuario:
            usuario.contrasena = hash_password(contrasena_nueva)
            db.session.commit()

            # Limpiar sesión
            session.pop("recovery_email", None)
            session.pop("recovery_codigo", None)
            session.pop("recovery_user_id", None)
            session.pop("codigo_verificado", None)

            flash(
                "Contraseña actualizada. Inicia sesión con tu nueva contraseña",
                "success",
            )
            return redirect(url_for("auth.login"))
        else:
            flash("Error al actualizar contraseña", "danger")
            return redirect(url_for("auth.recuperar_contraseña"))

    return render_template("usuario/nueva_contraseña.html")
