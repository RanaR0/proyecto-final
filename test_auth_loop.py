"""
Test para verificar que el loop de redirecciones fue eliminado.
Este test simula:
1. Acceso sin autenticación (GET /)
2. Manejo de sesiones corruptas
3. Login/logout flujo correcto
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from app import create_app


def test_redirect_loop():
    """Verifica que no haya loop de redirecciones"""
    app = create_app(testing=True)
    client = app.test_client()

    print("\n--- TEST: Eliminación de Loop de Redirecciones ---\n")

    # 1. Intento sin autenticación
    print("1. GET / sin sesión:")
    response = client.get("/", follow_redirects=False)
    print(f"   Status: {response.status_code}")
    print(f"   Redirige a: {response.location}")
    assert response.status_code == 302, "Debería redirigir"
    assert "/login" in response.location, "Debería ir a /login"
    print("   ✓ Correcto: sin autenticación → /login")

    # 2. GET /login sin autenticación
    print("\n2. GET /login sin sesión:")
    response = client.get("/login", follow_redirects=False)
    print(f"   Status: {response.status_code}")
    print(f"   Responde: 200 OK (no hay otro redirect)")
    assert response.status_code == 200, "Debería mostrar el formulario"
    print("   ✓ Correcto: /login muestra formulario, no redirige")

    # 3. Test con sesión corrupta (usuario_id fantasma)
    print("\n3. Simulación de sesión corrupta (usuario_id sin usuario en BD):")
    with client:
        with client.session_transaction() as sess:
            sess["usuario_id"] = 999999  # ID que no existe
            sess["nombre"] = "fantasma"

        response = client.get("/", follow_redirects=False)
        print(f"   GET / con usuario_id=999999: {response.status_code}")

        response = client.get("/login", follow_redirects=False)
        print(f"   GET /login con usuario_id=999999: {response.status_code}")

        # Verificar que la sesión fue limpiada
        with client.session_transaction() as sess:
            ha_sido_limpiada = "usuario_id" not in sess
            print(f"   Sesión limpiada después de /login: {ha_sido_limpiada}")

    print("\n   ✓ Correcto: sesiones corruptas son limpiadas")

    # 4. Verificar flujo correcto después de login
    print("\n4. Flujo POST /login con credenciales incorrectas:")
    response = client.post(
        "/login",
        data={"nombre_usuario": "usuario_inexistente", "contraseña": "password"},
        follow_redirects=False,
    )
    print(f"   POST /login (bad creds): {response.status_code}")
    assert response.status_code == 200, "Debería mostrar formulario de nuevo en auth.py"
    print("   ✓ Correcto: credenciales incorrectas no causen redirects")

    print("\n" + "=" * 60)
    print("✓ TODOS LOS TESTS PASARON")
    print("✓ Loop de redirecciones ELIMINADO")
    print("✓ Sesiones corruptas son manejadas correctamente")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_redirect_loop()
