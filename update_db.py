#!/usr/bin/env python
"""
Script para actualizar la base de datos con el nuevo campo creador_original.

Si la base de datos no tiene el campo creador_original, lo agregará automáticamente.
"""

import os
import sys
from sqlalchemy import inspect, text

# Configurar path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from app import create_app
from database import db
from models.receta import Receta


def update_database():
    """Actualiza la base de datos con el nuevo esquema."""
    app = create_app()

    with app.app_context():
        # Verificar si la tabla RECETAS existe
        inspector = inspect(db.engine)

        if "RECETAS" in inspector.get_table_names():
            print("✓ Tabla RECETAS encontrada")

            # Obtener columnas existentes
            columns = [col["name"] for col in inspector.get_columns("RECETAS")]
            print(f"  Columnas existentes: {columns}")

            # Verificar si el campo creador_original existe
            if "creador_original" not in columns:
                print("⚠ Campo 'creador_original' no encontrado. Agregando...")

                try:
                    # Usar SQL puro para agregar la columna con text()
                    with db.engine.connect() as connection:
                        connection.execute(
                            text(
                                "ALTER TABLE RECETAS ADD COLUMN creador_original VARCHAR(50)"
                            )
                        )
                        connection.commit()
                    print("✓ Campo 'creador_original' agregado exitosamente")

                except Exception as e:
                    print(f"✗ Error al agregar columna: {str(e)}")
                    print("  Consejo: Elimina instance/cocina.db y reinicia la app")
                    return False
            else:
                print("✓ Campo 'creador_original' ya existe")
        else:
            print("ℹ Tabla RECETAS no existe. Se creará automáticamente...")
            db.create_all()
            print("✓ Base de datos creada exitosamente")

    print("\n✅ Base de datos actualizada correctamente")
    return True


if __name__ == "__main__":
    success = update_database()
    sys.exit(0 if success else 1)
