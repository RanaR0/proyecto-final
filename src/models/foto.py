from database import db

# ---------------------------- Foto_receta ------------------------------ #


class Foto(db.Model):
    __tablename__ = "FOTOS"

    id = db.Column(db.Integer, primary_key=True)
    fecha_subida = db.Column(db.DateTime, server_default=db.func.now())
    foto = db.Column(db.String(255), nullable=False)

    id_paso = db.Column(
        db.Integer, db.ForeignKey("PASOS.id", ondelete="CASCADE"), nullable=False
    )

    paso = db.relationship("Paso", back_populates="fotos")

    def __init__(self, foto, id_paso):
        self.foto = foto
        self.id_paso = id_paso

    def __repr__(self):
        return f"<Foto id={self.id} id_paso={self.id_paso}>"
