from database import db

# ---------------------------- PASO ------------------------------ #


class Paso(db.Model):
    __tablename__ = "PASOS"

    id = db.Column(db.Integer, primary_key=True)
    num_paso = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.String(500), nullable=False)

    # 1. El campo físico que se guarda en la base de datos (Llave Foránea)
    id_receta = db.Column(
        db.Integer, db.ForeignKey("RECETAS.id", ondelete="CASCADE"), nullable=False
    )

    # 2. La relación (el objeto Receta) para navegar en Python
    receta = db.relationship("Receta", back_populates="pasos")

    # 3. Relación con fotos (asegúrate de que en la clase 'Foto' exista back_populates="paso")
    fotos = db.relationship("Foto", back_populates="paso", cascade="all, delete-orphan")
