import os
import ssl
import smtplib
import json
from email.message import EmailMessage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
SMTP_CONFIG_FILE = os.path.join(INSTANCE_DIR, "smtp_config.json")


def _ensure_instance_folder():
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR, exist_ok=True)


def _parse_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def load_smtp_settings():
    _ensure_instance_folder()
    if not os.path.exists(SMTP_CONFIG_FILE):
        return {
            "host": None,
            "port": None,
            "user": None,
            "password": None,
            "from_address": None,
            "use_tls": True,
            "use_ssl": False,
        }

    try:
        with open(SMTP_CONFIG_FILE, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
    except Exception:
        return {
            "host": None,
            "port": None,
            "user": None,
            "password": None,
            "from_address": None,
            "use_tls": True,
            "use_ssl": False,
        }

    return {
        "host": data.get("host"),
        "port": int(data["port"]) if data.get("port") else None,
        "user": data.get("user"),
        "password": data.get("password"),
        "from_address": data.get("from_address"),
        "use_tls": _parse_bool(data.get("use_tls"), True),
        "use_ssl": _parse_bool(data.get("use_ssl"), False),
    }


def save_smtp_settings(settings):
    _ensure_instance_folder()
    payload = {
        "host": settings.get("host"),
        "port": int(settings.get("port")) if settings.get("port") else None,
        "user": settings.get("user"),
        "password": settings.get("password"),
        "from_address": settings.get("from_address"),
        "use_tls": _parse_bool(settings.get("use_tls"), True),
        "use_ssl": _parse_bool(settings.get("use_ssl"), False),
    }

    with open(SMTP_CONFIG_FILE, "w", encoding="utf-8") as archivo:
        json.dump(payload, archivo, indent=2)

    return True


def get_smtp_config():
    env = {
        "host": os.getenv("SMTP_HOST"),
        "port": int(os.getenv("SMTP_PORT", "0")) if os.getenv("SMTP_PORT") else None,
        "user": os.getenv("SMTP_USER"),
        "password": os.getenv("SMTP_PASSWORD"),
        "from_address": os.getenv("SMTP_FROM"),
        "use_tls": _parse_bool(os.getenv("SMTP_USE_TLS"), True),
        "use_ssl": _parse_bool(os.getenv("SMTP_USE_SSL"), False),
    }
    file_cfg = load_smtp_settings()

    return {
        "host": env["host"] or file_cfg["host"],
        "port": env["port"] or file_cfg["port"],
        "user": env["user"] or file_cfg["user"],
        "password": env["password"] or file_cfg["password"],
        "from_address": env["from_address"] or file_cfg["from_address"],
        "use_tls": (
            env["use_tls"]
            if os.getenv("SMTP_USE_TLS") is not None
            else file_cfg["use_tls"]
        ),
        "use_ssl": (
            env["use_ssl"]
            if os.getenv("SMTP_USE_SSL") is not None
            else file_cfg["use_ssl"]
        ),
    }


def is_smtp_configured():
    cfg = get_smtp_config()
    return all(
        [cfg["host"], cfg["port"], cfg["user"], cfg["password"], cfg["from_address"]]
    )


def send_email(to_address, subject, body, html_body=None):
    """Envía un correo usando la configuración SMTP definida en variables de entorno o archivo local."""
    cfg = get_smtp_config()
    if not is_smtp_configured():
        return (
            False,
            "SMTP no está configurado. Define SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD y SMTP_FROM, o guarda la configuración en el panel de ajustes.",
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = cfg["from_address"]
    message["To"] = to_address
    message.set_content(body)

    if html_body:
        message.add_alternative(html_body, subtype="html")

    try:
        if cfg["use_ssl"]:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(cfg["host"], cfg["port"], context=context) as smtp:
                smtp.login(cfg["user"], cfg["password"])
                smtp.send_message(message)
        else:
            with smtplib.SMTP(cfg["host"], cfg["port"]) as smtp:
                if cfg["use_tls"]:
                    smtp.starttls(context=ssl.create_default_context())
                smtp.login(cfg["user"], cfg["password"])
                smtp.send_message(message)
        return True, "Correo enviado correctamente."
    except Exception as exc:
        return False, f"Error al enviar correo: {str(exc)}"
