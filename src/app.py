import os
import unittest
from flask import Flask
from database import db
from routes.auth import auth_bp
from routes.cuenta import cuenta_bp
from routes.crear import crear_bp
from services import esta_autenticado, obtener_usuario_actual


def create_app(testing=False):
    app = Flask(
        __name__, static_folder=os.path.join(os.path.dirname(__file__), "static")
    )
    app.secret_key = "dw2"

    # Configuración dinámica
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///:memory:"  # Base de datos volátil para tests
        )
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL", "sqlite:///cocina.db"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Extensiones y Blueprints
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cuenta_bp)
    app.register_blueprint(crear_bp)
    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_user():
        return dict(usuario=obtener_usuario_actual(), autenticado=esta_autenticado())

    return app


# Instancia global para que el servidor web la encuentre siempre
app = create_app()

if __name__ == "__main__":
    # --- BLOQUE DE TESTEO FUNCIONAL ---
    print("Ejecutando pruebas funcionales antes de iniciar...")

    # Definimos una clase de test rápida dentro del main para validar rutas críticas
    class ProyectoTest(unittest.TestCase):
        def setUp(self):
            self.app_test = create_app(testing=True)
            self.client = self.app_test.test_client()

    # Ejecutar tests
    suite = unittest.TestLoader().loadTestsFromTestCase(ProyectoTest)
    resultado = unittest.TextTestRunner(verbosity=1).run(suite)

    if resultado.wasSuccessful():
        print("Tests pasados. Iniciando servidor en http://127.0.0.1:5000")
        app.run(debug=True)
    else:
        print("Tests fallidos. Revisa tu lógica antes de iniciar.")
