import os
from werkzeug.utils import secure_filename

# Paths fijos para el static dentro de src
BASE_DIR = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

# Funciones para manejar la estructura de carpetas de uploads


def get_user_folder(user_id):
    """Retorna la ruta de la carpeta del usuario."""
    return os.path.join(STATIC_ROOT, "uploads", str(user_id))


def get_profile_photo_folder(user_id):
    """Retorna la ruta de la carpeta de foto de perfil del usuario."""
    return os.path.join(get_user_folder(user_id), "perfil")


def get_recipes_folder(user_id):
    """Retorna la ruta de la carpeta de recetas del usuario."""
    return os.path.join(get_user_folder(user_id), "recetas")


def get_recipe_folder(user_id, recipe_id):
    """Retorna la ruta de la carpeta de una receta específica."""
    return os.path.join(get_recipes_folder(user_id), str(recipe_id))


def get_steps_folder(user_id, recipe_id):
    """Retorna la ruta de la carpeta de pasos de una receta específica."""
    return os.path.join(get_recipe_folder(user_id, recipe_id), "pasos")


def ensure_folder_exists(folder_path):
    """Asegura que la carpeta exista, creándola si no."""
    os.makedirs(folder_path, exist_ok=True)


def save_uploaded_file(file, folder_path, filename):
    """Guarda un archivo subido en la carpeta especificada y retorna la ruta relativa.

    Usa secure_filename para prevenir path traversal (OWASP A01).
    """
    safe_name = secure_filename(filename)
    if not safe_name:
        raise ValueError("Nombre de archivo no válido o vacío.")
    ensure_folder_exists(folder_path)
    file_path = os.path.join(folder_path, safe_name)
    file.save(file_path)
    # Retorna la ruta relativa desde static/
    return os.path.relpath(file_path, STATIC_ROOT).replace("\\", "/")


def get_static_root():
    """Retorna la carpeta static que está dentro de src."""
    return STATIC_ROOT
