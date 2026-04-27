# 📦 Separación de Scripts JS Inline a Estáticos

## ✅ Cambios Realizados

Se extrajeron todos los scripts inline de los templates HTML y se movieron a archivos JS separados en la carpeta `static/js/`. Esto mejora la organización, mantenibilidad y aprovecha el caché del navegador.

---

## 📝 Archivos JS Creados

### 1. **crearRecetasUI.js**
Manejo de la UI para crear recetas:
- Click en foto principal → abre input de archivo
- Preview de imagen seleccionada
- **Usado en**: `crear.html`

### 2. **editarRecetasUI.js**
Manejo de la UI para editar recetas:
- Selector de versiones con confirmación
- Click en foto principal → abre input de archivo
- Preview de imagen seleccionada
- **Usado en**: `editar.html`

### 3. **layoutTheme.js**
Gestión global del tema oscuro/claro:
- Detecta preferencia del sistema
- Persiste selección en localStorage
- Aplica clases CSS `dark` dinámicamente
- **Usado en**: `layout.html`

### 4. **alertas.js**
Funciones de la página de alertas:
- `guardarAlertas()` - Muestra alerta de funcionalidad futura
- **Usado en**: `alertas.html`

### 5. **busqueda.js**
Funcionalidad de búsqueda de recetas:
- Infinite scroll para cargar más recetas
- Búsqueda en tiempo real por nombre
- Peticiones AJAX a `/api/busqueda`
- **Usado en**: `busqueda.html`

### 6. **perfil.js**
Funciones de la página de perfil:
- `mostrarTab(tab)` - Cambio dinámico de pestañas
- Gestiona estilos activos/inactivos
- **Usado en**: `perfil.html`

### 7. **privacidad.js**
Funciones de la página de privacidad:
- `guardarPrivacidad()` - Muestra alerta de funcionalidad futura
- **Usado en**: `privacidad.html`

---

## 📁 Estructura de Archivos

```
static/js/
├── account-theme.js          (existente)
├── crearRecetas.js           (existente)
├── crearRecetasUI.js         (nuevo)
├── editarRecetasUI.js        (nuevo)
├── layoutTheme.js            (nuevo)
├── alertas.js                (nuevo)
├── busqueda.js               (nuevo)
├── perfil.js                 (nuevo)
├── privacidad.js             (nuevo)
├── recipes-theme.js          (existente)
├── theme.js                  (existente)
└── vistaRecetas.js           (existente)
```

---

## 🔄 Cambios en Templates

### crear.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/crearRecetasUI.js') }}"></script>
```

### editar.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/editarRecetasUI.js') }}"></script>
```

### layout.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/layoutTheme.js') }}"></script>
```

### alertas.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/alertas.js') }}"></script>
```

### busqueda.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/busqueda.js') }}"></script>
```

### perfil.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/perfil.js') }}"></script>
```

### privacidad.html
```html
<!-- ❌ Antes -->
<script> ... código inline ... </script>

<!-- ✅ Después -->
<script src="{{ url_for('static', filename='js/privacidad.js') }}"></script>
```

---

## 📊 Estadísticas

| Métrica | Antes | Después |
|---------|-------|---------|
| Scripts inline | 7 | 0 |
| Archivos JS estáticos | 5 | 12 |
| Líneas inline en HTML | ~150 | 0 |
| Tamaño de JS | x5 | Mejor caché |

---

## ✨ Beneficios

✅ **Mejor Mantenibilidad**: Scripts organizados y fáciles de localizar
✅ **Mejor Caché**: El navegador cachea archivos JS por más tiempo
✅ **Menor HTML**: Los templates son más limpios y legibles
✅ **Reutilización**: Los scripts pueden usarse en múltiples páginas
✅ **Debugging**: Más fácil depurar con DevTools
✅ **Rendimiento**: Los scripts se cargan después del HTML

---

## 🧪 Validación

- ✅ Aplicación carga correctamente
- ✅ Todos los scripts están en la carpeta `static/js`
- ✅ No hay scripts inline en los templates
- ✅ Funcionalidad preservada al 100%
- ✅ Consistencia con estructura existente

---

## 🚀 Próximos Pasos (Opcional)

Si deseas optimizar aún más:
1. **Minificar JS**: Usar herramientas como `terser` o `uglify`
2. **Combinar JS**: Agrupar archivos relacionados
3. **Lazy Load**: Cargar scripts solo cuando sea necesario
4. **Service Worker**: Cachear scripts estáticos

---

**¡Scripts separados correctamente! 🎉**
