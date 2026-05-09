"""
Script de desarrollo para ejecutar la aplicación en modo DEV con base de datos de prueba.

Características:
- Usa una BD separada (cocina_dev.db) que no afecta la producción
- Genera datos de testeo automáticamente
- Comprueba errores e imports antes de iniciar
- Debug mode habilitado
- Color-coded output para mejor legibilidad

Uso: python dev.py
"""

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path


# Colores para terminal
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    """Imprime un encabezado con formato"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text):
    """Imprime mensaje informativo"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def check_imports():
    """Verifica que todos los imports necesarios estén disponibles"""
    print_header("1. VERIFICANDO IMPORTS")

    imports_to_check = [
        ("flask", "Flask"),
        ("flask_sqlalchemy", "Flask-SQLAlchemy"),
        ("werkzeug", "Werkzeug"),
    ]

    all_ok = True
    for module, name in imports_to_check:
        try:
            __import__(module)
            print_success(f"{name} disponible")
        except ImportError:
            print_error(f"{name} NO ENCONTRADO")
            all_ok = False

    # Verificar módulos locales
    local_modules = ["database", "models", "routes", "services"]
    for module in local_modules:
        try:
            __import__(module)
            print_success(f"Módulo local '{module}' disponible")
        except ImportError as e:
            print_error(f"Módulo local '{module}' NO ENCONTRADO: {e}")
            all_ok = False

    return all_ok


def check_file_structure():
    """Verifica que la estructura de archivos sea correcta"""
    print_header("2. VERIFICANDO ESTRUCTURA DE ARCHIVOS")

    required_files = [
        "app.py",
        "database.py",
        "models/__init__.py",
        "models/usuario.py",
        "models/receta.py",
        "models/pasos.py",
        "routes/__init__.py",
        "routes/auth.py",
        "routes/cuenta.py",
        "routes/crear.py",
        "services/__init__.py",
        "static",
        "templates",
    ]

    all_ok = True
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} NO ENCONTRADO")
            all_ok = False

    return all_ok


def setup_dev_database():
    """Crea la BD de desarrollo con datos de testeo"""
    print_header("3. CONFIGURANDO BASE DE DATOS DE DESARROLLO")

    # Ruta de BD de desarrollo
    instance_dir = Path("instance")
    instance_dir.mkdir(exist_ok=True)

    db_path = instance_dir / "cocina_dev.db"

    # Eliminar BD anterior si existe
    if db_path.exists():
        print_warning(f"BD anterior encontrada, recreando...")
        db_path.unlink()

    print_info(f"Creando BD en: {db_path.absolute()}")

    # Retornar la ruta relativa para SQLAlchemy
    return "cocina_dev.db"


def generate_test_data():
    """Genera datos de testeo en la BD"""
    print_header("4. GENERANDO DATOS DE TESTEO")

    try:
        from app import create_app, db
        from models.usuario import Usuario
        from models.receta import Receta
        from models.ingrediente import Ingrediente
        from models.receta_ingrediente import Receta_Ingrediente
        from models.pasos import Paso

        # Crear app con BD dev
        (
            os.chdir("..") if Path("database.py").exists() == False else None
        )  # Cambiar a src si es necesario
        app = create_app()

        # Modificar la URI de la BD hacia la versión dev
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cocina_dev.db"

        with app.app_context():
            # Crear tablas
            db.drop_all()
            db.create_all()
            print_success("Tablas creadas")

            # --- USUARIOS DE TESTEO ---
            users = [
                Usuario(
                    nombre="Carlos",
                    apellidos="García López",
                    usuario="carlos_chef",
                    contrasena="123456",
                    gmail="carlos@test.com",
                    descripcion="Chef apasionado por la cocina italiana",
                ),
                Usuario(
                    nombre="María",
                    apellidos="Rodríguez Martín",
                    usuario="maria_cook",
                    contrasena="123456",
                    gmail="maria@test.com",
                    descripcion="Especialista en repostería y postres",
                ),
                Usuario(
                    nombre="Juan",
                    apellidos="López Fernández",
                    usuario="juan_gourmet",
                    contrasena="123456",
                    gmail="juan@test.com",
                    descripcion="Amante de la gastronomía moderna",
                ),
            ]

            for user in users:
                db.session.add(user)
            db.session.commit()
            print_success(f"{len(users)} usuarios de testeo creados")

            # --- RECETAS DE TESTEO ---
            recetas_data = [
                {
                    "nombre": "Pasta Carbonara",
                    "descripcion": "Clásica receta italiana con huevo, queso y panceta",
                    "tiempo": 20,
                    "raciones": "4",
                    "categoria": "Italiana",
                    "usuario_id": 1,
                    "pasos": [
                        "Cocina la pasta en agua salada",
                        "Fríe la panceta hasta que esté crujiente",
                        "Mezcla huevos con queso parmesano",
                        "Combina todo mientras la pasta está caliente",
                    ],
                    "ingredientes": ["Pasta", "Huevos", "Queso", "Panceta", "Pimienta"],
                },
                {
                    "nombre": "Tiramisú",
                    "descripcion": "Postre italiano tradicional con capas de queso y café",
                    "tiempo": 30,
                    "raciones": "8",
                    "categoria": "Postres",
                    "usuario_id": 2,
                    "pasos": [
                        "Mezcla yemas de huevo con azúcar",
                        "Añade queso mascarpone",
                        "Moja los bizcochos en café",
                        "Alterna capas de bizcochos y crema",
                        "Refrigera 4 horas",
                    ],
                    "ingredientes": [
                        "Bizcochos",
                        "Café",
                        "Huevos",
                        "Azúcar",
                        "Mascarpone",
                    ],
                },
                {
                    "nombre": "Tacos Al Pastor",
                    "descripcion": "Sabrosos tacos mexicanos con carne marinada",
                    "tiempo": 45,
                    "raciones": "6",
                    "categoria": "Mexicana",
                    "usuario_id": 3,
                    "pasos": [
                        "Prepara la marinada con especias",
                        "Marina la carne 2 horas",
                        "Asa la carne en la plancha",
                        "Calienta las tortillas",
                        "Sirve con cebolla y cilantro",
                    ],
                    "ingredientes": [
                        "Carne de cerdo",
                        "Tortillas",
                        "Especias",
                        "Cebolla",
                        "Cilantro",
                    ],
                },
            ]

            for recipe_data in recetas_data:
                pasos = recipe_data.pop("pasos")
                ingredientes = recipe_data.pop("ingredientes")
                usuario_id = recipe_data.pop("usuario_id")

                receta = Receta(
                    id_propietario=usuario_id,
                    nombre=recipe_data["nombre"],
                    tipo="normal",
                    categoria=recipe_data["categoria"],
                    descripcion=recipe_data["descripcion"],
                    tiempo=recipe_data["tiempo"],
                    raciones=recipe_data["raciones"],
                )
                db.session.add(receta)
                db.session.flush()

                # Agregar pasos
                for idx, paso_text in enumerate(pasos, 1):
                    paso = Paso(num_paso=idx, texto=paso_text, id_receta=receta.id)
                    db.session.add(paso)

                # Agregar ingredientes
                for ing_name in ingredientes:
                    ingrediente = Ingrediente.query.filter_by(nombre=ing_name).first()
                    if not ingrediente:
                        ingrediente = Ingrediente(nombre=ing_name)
                        db.session.add(ingrediente)
                        db.session.flush()

                    rel = Receta_Ingrediente(
                        id_receta=receta.id,
                        id_ingrediente=ingrediente.id,
                        cantidad="",
                        unidad="",
                    )
                    db.session.add(rel)

            db.session.commit()
            print_success(f"{len(recetas_data)} recetas de testeo creadas")

            # Mostrar estadísticas
            user_count = Usuario.query.count()
            recipe_count = Receta.query.count()
            print_info(f"Total en BD: {user_count} usuarios, {recipe_count} recetas")

        return True

    except Exception as e:
        print_error(f"Error generando datos de testeo: {e}")
        import traceback

        traceback.print_exc()
        return False


def check_models():
    """Verifica la integridad de los modelos"""
    print_header("5. VERIFICANDO MODELOS")

    try:
        from models.usuario import Usuario
        from models.receta import Receta
        from models.pasos import Paso
        from models.ingrediente import Ingrediente
        from models.receta_ingrediente import Receta_Ingrediente

        models = [
            ("Usuario", Usuario),
            ("Receta", Receta),
            ("Paso", Paso),
            ("Ingrediente", Ingrediente),
            ("Receta_Ingrediente", Receta_Ingrediente),
        ]

        for name, model in models:
            try:
                # Verificar que el modelo tenga __tablename__
                if hasattr(model, "__tablename__"):
                    print_success(f"Modelo '{name}' OK")
                else:
                    print_warning(f"Modelo '{name}' podría tener problemas")
            except Exception as e:
                print_error(f"Error en modelo '{name}': {e}")
                return False

        return True

    except ImportError as e:
        print_error(f"Error importando modelos: {e}")
        return False


def start_dev_server():
    """Inicia el servidor de desarrollo"""
    print_header("6. INICIANDO SERVIDOR DE DESARROLLO")

    try:
        # Importar después de estar en src
        from app import create_app

        app = create_app()
        # Forzar la BD de desarrollo
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cocina_dev.db"

        print_success("Aplicación cargada correctamente")
        print_info(f"BD de desarrollo: instance/cocina_dev.db")
        print_info(f"Modo Debug: ACTIVO")
        print_info(f"URL: http://127.0.0.1:5000")
        print_info(f"Panel de administración: http://127.0.0.1:5000/admin (si existe)")

        print("\n" + Colors.BOLD + Colors.YELLOW)
        print("Credenciales de testeo:")
        print("  usuario: carlos_chef, contraseña: 123456")
        print("  usuario: maria_cook, contraseña: 123456")
        print("  usuario: juan_gourmet, contraseña: 123456")
        print(Colors.RESET)

        print_info("Presiona CTRL+C para detener el servidor\n")

        app.run(debug=True, use_reloader=True)

    except Exception as e:
        print_error(f"Error iniciando servidor: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


def main():
    """Función principal"""
    print_header("MODO DESARROLLO - COCINA RECETAS")
    print(f"{Colors.CYAN}Iniciando aplicación en modo desarrollo...{Colors.RESET}\n")

    # 1. Verificar imports
    if not check_imports():
        print_error(
            "\nAlgunos imports no están disponibles. Instala las dependencias con:"
        )
        print_info("pip install -r requirements.txt")
        sys.exit(1)

    # 2. Verificar estructura de archivos
    if not check_file_structure():
        print_error("\nLa estructura de archivos no es completa.")
        sys.exit(1)

    # 3. Configurar BD de desarrollo
    db_name = setup_dev_database()

    # 4. Verificar modelos
    if not check_models():
        print_error("\nHay errores en los modelos.")
        sys.exit(1)

    # 5. Generar datos de testeo
    if not generate_test_data():
        print_error("\nError generando datos de testeo.")
        sys.exit(1)

    # 6. Iniciar servidor
    if not start_dev_server():
        print_error("\nError iniciando el servidor.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Servidor detenido por el usuario.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
