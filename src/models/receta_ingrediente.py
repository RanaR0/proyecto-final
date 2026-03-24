from database import db

# ---------------------------- Receta_Ingrediente ------------------------------ #


class Receta_Ingrediente(db.Model):
    __tablename__ = "RECETAS_INGREDIENTES"

    id = db.Column(db.Integer, primary_key=True)

    id_receta = db.Column(db.Integer, db.ForeignKey("RECETAS.id", ondelete="CASCADE"), nullable=False)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey("INGREDIENTES.id", ondelete="CASCADE"), nullable=False)

    cantidad = db.Column(db.String(50), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)

    receta = db.relationship(
        "Receta", backref=db.backref("ingredientes_asociados", cascade="all, delete-orphan")
        )

    ingrediente = db.relationship(
        "Ingrediente", backref=db.backref("recetas_asociadas", cascade="all, delete-orphan")
        )