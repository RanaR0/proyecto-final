from database import db

# ---------------------------- USUARIO ------------------------------ #


class Usuario(db.Model):
    __tablename__ = "USUARIOS"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(75), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String, nullable=False)
    gmail = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(75), nullable=True)
    # foto_perfil =db.Columna(db.String())
    # Las relaciones (back_populates) permiten la navegación bidireccional
