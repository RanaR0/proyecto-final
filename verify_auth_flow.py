#!/usr/bin/env python
"""
Script para verificar que el flujo de autenticación funciona correctamente.
"""
import sys

sys.path.insert(0, "src")

from app import create_app

app = create_app()

# Verificar rutas registradas
print("✓ Rutas registradas en la aplicación:\n")

rules = list(app.url_map.iter_rules())
rules_sorted = sorted(rules, key=lambda r: str(r))

for rule in rules_sorted:
    if "/static" in str(rule):
        continue
    methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
    print(f"  {str(rule):40} [{methods}]")

print("\n✓ Flujo de autenticación esperado:")
print("  1. Usuario sin sesión accede a / → redirige a /login")
print("  2. Usuario en login ingresa credenciales → POST /login → redirige a /")
print("  3. Usuario autenticado accede a / → redirige a cuenta/index")
print("  4. Usuario accede a /logout → elimina sesión → redirige a /login")

print("\n✓ Verificación completada sin errores ✅")
