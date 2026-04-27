# Modo Desarrollo - Guía de Uso

## ¿Qué es `dev.py`?

`dev.py` es un script de desarrollo que automatiza la configuración del entorno de prueba local. Crea una base de datos separada (`cocina_dev.db`) con datos de testeo, valida la integridad del proyecto y proporciona un servidor Flask con debug activado.

---

## Características

✅ **Base de datos independiente** - No afecta la BD de producción
✅ **Datos de testeo automáticos** - 3 usuarios + 3 recetas con datos realistas
✅ **Validación completa** - Verifica imports, estructura de archivos y modelos
✅ **Debug activado** - Reload automático y mejor manejo de errores
✅ **Output con colores** - Fácil lectura de mensajes y estado
✅ **Credenciales de testeo** - Lisadas al iniciar el servidor

---

## Cómo usar

### Opción 1: Desde PowerShell (recomendado)

```powershell
cd src
python dev.py
```

### Opción 2: Desde cualquier carpeta

```powershell
python src/dev.py
```

### Opción 3: Crear un alias (Windows)

Agrega esto a tu perfil de PowerShell (`$PROFILE`):

```powershell
function dev { cd c:\Users\Usuario\OneDrive\Documentos\DW2\PYTHON\ssss\proyecto.final.python-main\src ; python dev.py }
```

Luego desde cualquier terminal:
```powershell
dev
```

---

## Pasos que ejecuta automáticamente

1. **Verify Imports** - Comprueba que Flask, SQLAlchemy y otros módulos estén instalados
2. **Check File Structure** - Valida que todos los archivos necesarios existan
3. **Setup Dev Database** - Crea `instance/cocina_dev.db` limpia
4. **Check Models** - Verifica que los modelos SQLAlchemy sean válidos
5. **Generate Test Data** - Inserta usuarios y recetas de prueba
6. **Start Dev Server** - Inicia Flask en `http://127.0.0.1:5000`

---

## Credenciales de testeo

Una vez que `dev.py` termine de inicializar, verás en la consola:

```
Credenciales de testeo:
  usuario: carlos_chef, contraseña: 123456
  usuario: maria_cook, contraseña: 123456
  usuario: juan_gourmet, contraseña: 123456
```

Úsalas para probar la app sin crear cuentas nuevas.

---

## Base de datos de testeo

| Campo | Valor |
|-------|-------|
| Ubicación | `instance/cocina_dev.db` |
| Sobrescrita | Sí (cada vez que ejecutas dev.py) |
| Usuarios | 3 |
| Recetas | 3 (con pasos e ingredientes) |

### Datos incluidos:

**Usuarios:**
- carlos_chef: Chef especialista en italiana
- maria_cook: Especialista en repostería
- juan_gourmet: Amante de gastronomía moderna

**Recetas:**
- Pasta Carbonara (Carlos)
- Tiramisú (María)
- Tacos Al Pastor (Juan)

---

## Solución de problemas

### Error: "Module not found"

```
pip install -r requirements.txt
```

### Error: "Database not found"

Asegúrate de estar en el, carpeta `src`:
```powershell
cd C:\...\proyecto.final.python-main\src
python dev.py
```

### El servidor no inicia

1. Verifica que el puerto 5000 no esté en uso:
   ```powershell
   netstat -ano | findstr :5000
   ```

2. Si lo está, mata el proceso:
   ```powershell
   taskkill /PID <PID> /F
   ```

3. Intenta nuevamente.

---

## Diferencias: `app.py` vs `dev.py`

| Aspecto | app.py | dev.py |
|--------|--------|--------|
| BD | cocina.db (producción) | cocina_dev.db (testeo) |
| Datos iniciales | Los que creasx | 3 usuarios + 3 recetas auto |
| Debug | Depende del modo | Siempre activo |
| Validación | Mínima | Completa (6 pasos) |
| Reload | Depende de Reloader | Automático |

---

## Estructura de carpetas

```
proyecto.final.python-main/
├── src/
│   ├── app.py           # App principal
│   ├── dev.py           # Tema archivo (TÚ ERES AQUÍ)
│   ├── database.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   └── instance/
│       ├── cocina.db        # BD de producción
│       └── cocina_dev.db    # BD de testeo (creada por dev.py)
├── requirements.txt
└── README.md
```

---

## Tips útiles

### Acceder a la BD de testeo con SQLite

```powershell
sqlite3 "src/instance/cocina_dev.db"
```

Luego puedes consultar:
```sql
SELECT * FROM USUARIOS;
SELECT * FROM RECETAS;
```

### Ver logs en tiempo real

En la consola verás todos los requests y cambios mientras navegas la app.

### Mantener los datos de testeo

Los datos se regeneran cada vez que ejecutas `dev.py`. Si quieres preservar cambios, modifica `dev.py` para que no haga `db.drop_all()`.

### Usar una BD existente

Si ya testviste algo y quieres mantener la BD, renómbrala antes de ejecutar:

```powershell
Rename-Item "instance/cocina_dev.db" "instance/cocina_dev_backup.db"
```

---

## Próximos pasos

- Prueba el sistema de versionado de recetas
- Crea nuevas recetas y edítalas
- Prueba copiar recetas de otros usuarios
- Verifica el funcionamiento del sistema de amigos

---

¡Feliz desarrollo! 🚀
