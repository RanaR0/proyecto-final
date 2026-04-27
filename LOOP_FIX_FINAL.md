# ✓ SOLUCIÓN: Loop de Redirecciones Eliminado

## 🔴 Problema Original

**Síntoma:** Redirect infinito `GET / → 302 → GET /login → 302 → ...`
**Error en navegador:** "La página 127.0.0.1 te ha redirigido demasiadas veces"

## 🔍 Causa Raíz Identificada

El problema era una **sesión corrupta** donde `usuario_id` estaba en session pero el usuario NO existía en la BD.

### Flujo del Loop:
```
1. GET / → cuenta.index()
   └─ obtener_usuario_actual() retorna None (usuario_id fantasma)
   └─ redirect → GET /login

2. GET /login → auth.login()
   └─ esta_autenticado() retorna True (usuario_id SÍ está en session)
   └─ redirect → GET /

3. Vuelve al paso 1 → LOOP INFINITO
```

El inconveniente: la verificación en `/login` chequeaba si `usuario_id` existía en session, pero NO chequeaba si ese usuario existía en la BD.

## ✅ Soluciones Implementadas

### 1. **En `src/routes/auth.py` (función `login`)**

**Antes:**
```python
if esta_autenticado():
    return redirect(url_for("cuenta.index"))
```

**Ahora:**
```python
# Solo redirigir a /index si el usuario está autenticado Y existe en BD
from services import obtener_usuario_actual
if esta_autenticado() and obtener_usuario_actual():
    return redirect(url_for("cuenta.index"))

# Si hay una sesión corrupta (usuario_id pero sin usuario en BD), limpiarla
if "usuario_id" in session and not obtener_usuario_actual():
    session.clear()
```

**Qué hace:** Verifica tanto `esta_autenticado()` como que el usuario exista realmente en la BD. Si la sesión está corrupta, la limpia.

### 2. **En `src/routes/cuenta.py` (función `index`)**

**Antes:**
```python
if not usuario:
    return redirect(url_for("auth.login"))
```

**Ahora:**
```python
if not usuario:
    # Si hay una sesión corrupta, limpiarla
    if "usuario_id" in session:
        session.clear()
    return redirect(url_for("auth.login"))
```

**Qué hace:** Cuando hay un usuario fantasma, limpia la sesión antes de redirigir.

## 🧪 Verificación

Ejecutar test:
```bash
python test_auth_loop.py
```

**Resultados del test:**
- ✓ GET / sin sesión → redirige a /login (correcto)
- ✓ GET /login sin sesión → muestra formulario, NO redirige (correcto)
- ✓ Con usuario_id fantasma → sesión es limpiada (correcto)
- ✓ POST /login con creds incorrectas → muestra formulario, NO redirige (correcto)

## 📋 Flujo de Autenticación Ahora (Correcto)

```
No hay sesión:
  GET / → cuenta.index() → sin usuario → redirect("/login")
  GET /login → auth.login() → muestra formulario

Usuario intenta login:
  POST /login → login_usuario() → session["usuario_id"] = X
  → redirect("/") → cuenta.index() → usuario encontrado → render template

Ya estoy logueado:
  GET / → cuenta.index() → usuario existe → render template
  GET /login → auth.login() → ya autenticado → redirect("/")

Sesión corrupta:
  session["usuario_id"] = 999999 (no existe)
  GET /login → AUTH.LOGIN() → session.clear() → muestra formulario
  GET / → CUENTA.INDEX() → session.clear() → redirect("/login")
  (sin loop porque se limpió)
```

## 🔧 Cambios de Archivos

| Archivo | Cambio |
|---------|--------|
| `src/routes/auth.py` | Añadido chequeo de existencia en BD + limpieza de sesiones corruptas |
| `src/routes/cuenta.py` | Añadido limpieza de sesiones corruptas |
| `test_auth_loop.py` | Nuevo test para verificar NO hay redirects infinitos |

---

**Estado:** ✅ **FIXED**
**Fecha:** 13 de abril de 2026
