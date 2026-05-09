import sqlite3

conn = sqlite3.connect("../instance/cocina.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(USUARIOS)")
cols = cursor.fetchall()

print("Columnas en tabla USUARIOS:")
for col in cols:
    print(f"  {col[1]}: {col[2]}")

# Verificar específicamente si existen las columnas de privacidad
privacidad_cols = [
    "privacidad_seguir",
    "privacidad_recetas",
    "privacidad_interactuar",
    "privacidad_likes",
    "privacidad_seguidores",
]
col_names = [col[1] for col in cols]

print("\nVerificación de columnas de privacidad:")
for priv_col in privacidad_cols:
    exists = "✓" if priv_col in col_names else "✗"
    print(f"  {exists} {priv_col}")

conn.close()
