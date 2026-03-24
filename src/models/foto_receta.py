from database import db

# ---------------------------- Foto_receta ------------------------------ #


class Foto_receta(db.Model):
    __tablename__ = "FOTOS_RECETAS"

    id = db.Column(db.Integer, primary_key=True)

    id_receta = db.Column(db.Integer, db.ForeignKey("RECETAS.id", ondelete="CASCADE"), nullable=False)
    id_foto = db.Column(db.Integer, db.ForeignKey("FOTOS.id", ondelete="CASCADE"), nullable=False)
    id_paso = db.Column(db.Integer, nullable=True)

    receta = db.relationship(
      "Receta", backref=db.backref("fotos_asociadas", cascade="all, delete-orphan")
      )

    foto = db.relationship(
      "Foto", backref=db.backref("recetas_asociadas", cascade="all, delete-orphan")
      )