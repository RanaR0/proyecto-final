import os

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
    """Guarda un archivo subido en la carpeta especificada con el nombre dado y retorna la ruta relativa."""
    ensure_folder_exists(folder_path)
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)
    # Retorna la ruta relativa desde static/
    return os.path.relpath(file_path, STATIC_ROOT).replace("\\", "/")


def get_static_root():
    """Retorna la carpeta static que está dentro de src."""
    return STATIC_ROOT


# Funciones existentes (agregadas para evitar errores de importación)
def obtener_datos_grafico_saldo_evolutivo():
    """Función placeholder para obtener datos del gráfico de saldo evolutivo."""
    # Implementar según necesidad
    return []


def validar_datos_tarjeta_form():
    """Función placeholder para validar datos de formulario de tarjeta."""
    # Implementar según necesidad
    return True
