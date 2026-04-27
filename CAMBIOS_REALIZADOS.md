# Cambios Realizados: Control de Errores y Campo Creador en Recetas

## 📋 Resumen
Se implementó un sistema robusto de validación de errores, manejo de excepciones y un campo para rastrear el creador original de las recetas, incluso cuando se copian múltiples veces.

---

## 🔧 Cambios en el Modelo (models/receta.py)

### Nuevo Campo
- **`creador_original`** (String, nullable): Almacena el @usuario del creador principal de la receta
  - Para recetas originales: Se guarda como `@usuario` del propietario
  - Para copias: Se hereda y mantiene del creador original
  - Permite rastrear la fuente de una receta a través de múltiples copias

### Actualización del __init__
- Se agregó el parámetro `creador_original` al constructor de la clase

---

## ✅ Validaciones Implementadas (routes/crear.py)

### 1. **Función `validate_form_data()`**
Valida información principal de la receta:
- ✓ Título no vacío y máximo 50 caracteres
- ✓ Descripción no vacía y máximo 500 caracteres
- ✓ Tiempo de cocción válido (número)
- ✓ Porciones válidas (número)
- ✓ Categoría seleccionada

### 2. **Función `validate_ingredients()`**
- ✓ Al menos un ingrediente obligatorio
- ✓ Ingredientes no vacíos

### 3. **Función `validate_steps()`**
- ✓ Al menos un paso de instrucción obligatorio
- ✓ Pasos no vacíos

### 4. **Función `validate_image()`**
- ✓ Tipos de archivo permitidos: JPG, JPEG, PNG, GIF
- ✓ Tamaño máximo: 5MB
- ✓ Validación en fotos principales y de pasos

---

## 🛡️ Control de Errores

### Ruta `/guardar` (Crear Receta)
```python
- Verificación de usuario autenticado
- Validación completa de datos antes de guardar
- Try-except en creación de receta
- Try-except en cada ingrediente
- Try-except en cada paso y foto de paso
- Rollback automático en caso de error
- Mensajes de error descriptivos al usuario
```

### Ruta `/actualizar` (Editar Receta)
```python
- Verificación de usuario autenticado
- Verificación de permisos (propietario)
- Validación completa de datos
- Try-except en actualización de ingredientes
- Try-except en actualización de pasos
- Rollback automático en caso de error
- Manejo de validación de imágenes
```

### Ruta `/copiar` (Copiar Receta)
```python
- Verificación de usuario autenticado
- Validación de receta original
- Preservación del creador original
- Try-except en copia de ingredientes
- Try-except en copia de pasos y fotos
- Rastreo correcto de usuario_original_id (incluso para copias en cadena)
```

---

## 📝 Cambios en Templates

### crear.html & editar.html
**Nuevo Bloque de Flash Messages:**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
  - Mensajes de error (rojo con ⚠️)
  - Mensajes de éxito (verde con ✓)
  - Estilizados y posicionados en la esquina superior derecha
  - Desaparecen automáticamente
```

### editar.html - Información de Copia
Se actualiza para mostrar:
- La receta original de la que fue copiada
- **El creador original con `@usuario`** (nueva característica)

---

## 🔄 Flujo de Creador Original

### Ejemplo 1: Receta Copiada Una Sola Vez
```
Usuario A crea receta "Pasta Carbonara"
  ↓
Usuario B copia receta
  → creador_original = "@usuario_a"
  → usuario_original_id = A
```

### Ejemplo 2: Receta Copiada en Cadena
```
Usuario A crea receta "Pasta Carbonara"
  ↓
Usuario B copia receta (creador_original = "@usuario_a")
  ↓
Usuario C copia la copia de B
  → creador_original = "@usuario_a" (mantiene el original)
  → usuario_original_id = A (rastreo correcto)
```

---

## 🎯 Constantes de Validación

```python
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_TITLE_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 500
```

---

## 📱 Mensajes de Error Mostrados al Usuario

### Errores de Formulario
- "El título de la receta es obligatorio."
- "El título no puede exceder 50 caracteres."
- "La descripción es obligatoria."
- "Debes agregar al menos un ingrediente."
- "Debes agregar al menos un paso de instrucciones."
- "El tiempo de cocción debe ser un número válido."

### Errores de Archivo
- "Tipo de archivo no permitido. Solo se aceptan: jpg, jpeg, png, gif"
- "El archivo de imagen es demasiado grande (máximo 5MB)."

### Errores de Base de Datos
- "Error al guardar ingrediente: [detalles]"
- "Error al guardar paso: [detalles]"
- "Error inesperado al guardar la receta: [detalles]"

---

## ✨ Mejoras en la Experiencia de Usuario

1. **Feedback Inmediato**: Los errores se muestran al instante en notificaciones visuales
2. **Validación Previa**: Evita intentar guardar datos inválidos
3. **Rastrabilidad**: Se sabe quién creó la receta original incluso después de múltiples copias
4. **Recuperación Segura**: Los errores usan rollback para no corromper datos
5. **Claridad**: Mensajes descriptivos en español

---

## 🔍 Cómo Probar

1. **Crear una receta válida**: Debe guardarse exitosamente
2. **Intentar crear sin ingredientes**: Debe mostrar error
3. **Intentar crear sin pasos**: Debe mostrar error
4. **Subir archivo inválido**: Debe mostrar error
5. **Editar una receta**: Debe validar de igual forma
6. **Copiar una receta**: Debe mantener `@usuario` del creador original
7. **Copiar una copia**: Debe mantener el creador original de la cadena

---

## 📊 Impacto de los Cambios

| Aspecto | Antes | Después |
|--------|-------|--------|
| Validación | Mínima | Completa |
| Manejo de Errores | Fallos silenciosos | Rollback + Mensaje |
| Rastreo de Origen | Solo id | @usuario + id |
| UX en Errores | Redirección silenciosa | Notificación clara |
| Seguridad de Datos | Riesgo de corrupción | Transacciones seguras |

