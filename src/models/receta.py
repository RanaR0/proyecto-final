from database import db

# ---------------------------- Receta ------------------------------ #


class Receta(db.Model):
    __tablename__ = "RECETAS"  # Recomendado en plural para consistencia

    id = db.Column(db.Integer, primary_key=True)

    # Corregido el nombre de la tabla foránea (ajusta según tu clase Usuario)
    id_propietario = db.Column(
        db.Integer, db.ForeignKey("USUARIOS.id", ondelete="CASCADE"), nullable=False
    )

    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    # Eliminado unique=True para evitar errores al repetir descripciones o raciones
    descripcion = db.Column(db.String(500), nullable=False)
    tiempo = db.Column(db.Integer, nullable=False)
    raciones = db.Column(db.String(50), nullable=False)

    destacado = db.Column(db.Boolean, default=False)
    foto_principal = db.Column(db.String(255), nullable=True)

    # Relación bidireccional con los Pasos
    pasos = db.relationship(
        "Paso", back_populates="receta", cascade="all, delete-orphan"
    )
