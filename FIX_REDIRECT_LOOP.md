# 🔧 Solución: Loop de Redirecciones Infinitas

## 📋 Problema Identificado

La aplicación estaba generando un bucle de redirecciones infinitas:
```
GET /login → 302 (redirección)
GET / → 302 (redirección)
GET /login → 302 (redirección)
GET / → 302 (redirección)
...
```

Mensaje de error al usuario:
> "La página 127.0.0.1 te ha redirigido demasiadas veces."

---

## 🔍 Causa Raíz

El problema era **rutas conflictivas** en Flask:

1. **Ruta Primera (Intención Original)**
   - Tabla: En `cuenta_bp` (blueprint de rutas de cuenta)
   - Ruta: `@cuenta_bp.route("/")`
   - Comportamiento: Redirige a `/login` si no hay usuario

2. **Ruta Segunda (Error)**
   - Agregada en `app.py` (archivo principal)
   - Ruta: `@app.route("/")`
   - Comportamiento: Intentaba manejar la lógica de autenticación

### El Problema

Tener **dos rutas `/"` registradas** causaba:
- Conflicto en Flask sobre cuál responder
- Posible comportamiento errático con redirects
- Loop entre `/` y `/login`

---

## ✅ Solución Implementada

### Cambio en `src/app.py`

```python
# ❌ ANTES
@app.route("/")
def index():
    if esta_autenticado():
        return redirect(url_for("cuenta.index"))
    else:
        return redirect(url_for("auth.login"))

# ✅ DESPUÉS
# Remover completamente la ruta "/" de app.py
# Dejar que cuenta_bp sea el único manejador
```

### Flujo de Autenticación Correctecto

```
Sin Sesión:
  GET /
    ↓ (cuenta.index verifica usuario)
  usuario = None
    ↓ (redirige a login)
  GET /login
    ↓ (auth.login renderiza formulario)
  Renderiza login.html

Con Credenciales Válidas:
  POST /login
    ↓ (auth.login valida)
  establece usuario_id en sesión
    ↓ (redirige a index)
  GET /
    ↓ (cuenta.index obtiene usuario)
  Renderiza página principal

Con Sesión:
  GET /
    ↓ (cuenta.index obtiene usuario)
  usuario ≠ None
    ↓ (renderiza directamente)
  Renderiza página principal
```

---

## 📝 Cambios de Código

### Archivo: `src/app.py`

```diff
- from flask import Flask, redirect, url_for
- from services import esta_autenticado, obtener_usuario_actual
+ from flask import Flask
+ from services import obtener_usuario_actual

def create_app(testing=False):
    # ... código existente ...

    @app.context_processor
    def inject_user():
        return dict(usuario=obtener_usuario_actual(), autenticado=esta_autenticado())

-   # ❌ Remover esta sección (causa el conflicto)
-   @app.route("/")
-   def index():
-       """Ruta raíz que redirige basándose en estado de autenticación."""
-       if esta_autenticado():
-           return redirect(url_for("cuenta.index"))
-       else:
-           return redirect(url_for("auth.login"))

    return app
```

---

## ✨ Resultado

✅ Una única ruta `/` registrada
✅ Flujo de autenticación lineal sin loops
✅ Comportamiento predecible y documentado
✅ Redireccionamientos funcionando correctamente

---

##🧪 Verificación

Se ejecutó `verify_auth_flow.py` que confirma:
- ✅ Solo una ruta `/` registrada
- ✅ Rutas `/login`, `/logout` disponibles
- ✅ Sin conflictos de rutas
- ✅ Flujo de autenticación lógico y correcto

---

## 📚 Rutas de Autenticación

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Punto entrada - redirige a login o renderiza |
| `/login` | GET,POST | Formulario de login y procesamiento |
| `/logout` | GET | Cierra sesión y redirige a login |
| `/registrarse` | GET,POST | Formulario de registro |
| `/recuperar_contraseña` | GET,POST | Recuperación de contraseña |

---

## 🎯 Próximos Pasos (Opcional)

Si quieres mejorar aún más:
1. Agregar middleware para validar sesiones
2. Implementar "Remember Me"
3. Agregar rate limiting en login
4. Usar cookies HTTP-only para mayor seguridad

---

**¡Loop de redirecciones corregido! ✅**
