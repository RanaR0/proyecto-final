from database import db

# ---------------------------- Foto_receta ------------------------------ #


class Foto(db.Model):
    __tablename__ = "FOTOS"

    id = db.Column(db.Integer, primary_key=True)
    fecha_subida = db.Column(db.DateTime, server_default=db.func.now())
    foto = db.Column(db.String(255), nullable=False)

    id_paso = db.Column(
        db.Integer,
        db.ForeignKey("PASOS.id", ondelete="CASCADE"),
        nullable=False
    )

    paso = db.relationship("Paso", back_populates="fotos")