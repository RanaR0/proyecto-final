# Sistema de Gestión de Recetas – Aplicación Web

**Python | Flask | SQLAlchemy ORM | TailwindCSS | 2026**

Aplicación web completa para la creación, gestión y visualización de recetas culinarias. Incluye autenticación de usuarios, sistema de favoritos, interfaz moderna y una arquitectura modular orientada a la escalabilidad y buenas prácticas.

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd proyecto-final
```

### 2. Instalar dependencias

```bash
python -m pip install flask flask-sqlalchemy werkzeug
```

### 3. Configurar SMTP opcional (para recuperación de contraseña)

Configura estas variables de entorno si quieres que la app envíe códigos de recuperación por email:

```bash
set SMTP_HOST=smtp.tuservidor.com
set SMTP_PORT=587
set SMTP_USER=tu_usuario
set SMTP_PASSWORD=tu_contraseña
set SMTP_FROM=tu@correo.com
set SMTP_USE_TLS=true
set SMTP_USE_SSL=false
```

> Si usas Gmail, es probable que necesites una contraseña de aplicación y `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`.
>
> También puedes guardar los datos SMTP desde la aplicación en el panel de ajustes, sin modificar variables de entorno.

### 4. Ejecutar la aplicación

```bash
python src/app.py
```

La base de datos y las carpetas necesarias se generan automáticamente al iniciar la aplicación.

---

## Descripción del Proyecto

Este proyecto implementa una plataforma web para gestionar recetas de cocina de forma intuitiva. Los usuarios pueden crear, explorar y guardar recetas favoritas dentro de un entorno visual moderno y responsive.

La aplicación está construida con:

* Flask como framework backend
* SQLAlchemy como ORM
* TailwindCSS para el diseño de la interfaz

---

## Arquitectura

El proyecto sigue una arquitectura modular organizada en:

* Modelos (ORM): Definición de entidades y relaciones
* Servicios: Lógica de negocio
* Blueprints: Gestión de rutas
* Plantillas: HTML + TailwindCSS (Jinja2)

---

## Modelo de Datos

### Usuarios

* Datos personales y credenciales
* Relación con recetas creadas
* Relación con recetas favoritas

### Recetas

* Título, descripción, categoría, tiempo, raciones e imagen
* Relación con ingredientes y pasos
* Relación con el usuario propietario

### Ingredientes

* Nombre del ingrediente
* Relación muchos a muchos con recetas

### Pasos

* Número de paso y descripción
* Relación uno a muchos con recetas

### Favoritos

* Tabla intermedia `Receta_Usuario_Likes`
* Relación muchos a muchos entre usuarios y recetas

---

## Funcionalidades

### Autenticación

* Registro de usuarios
* Inicio de sesión con validación
* Cierre de sesión
* Contraseñas almacenadas mediante hashing seguro

### Gestión de Recetas

* Creación de recetas con ingredientes y pasos dinámicos
* Visualización en tarjetas responsivas
* Vista detallada de recetas

### Sistema de Favoritos

* Añadir y eliminar recetas favoritas
* Página dedicada a favoritos
* Icono dinámico (corazón lleno/vacío)

### Interfaz de Usuario

* Navbar de navegación
* Diseño moderno con TailwindCSS
* Formularios estilizados
* Diseño responsive

---

## Requisitos del Sistema

* Python 3.10 o superior
* Flask 2.x
* Flask-SQLAlchemy 3.x
* SQLAlchemy 2.0 o superior
* TailwindCSS (CDN)
* Werkzeug

---

## Buenas Prácticas Aplicadas

* Arquitectura modular con Blueprints
* Separación clara de responsabilidades
* Código siguiendo estándares PEP8
* Validación de datos y manejo de errores
* Uso eficiente de relaciones ORM





