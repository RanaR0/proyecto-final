from database import db

# ---------------------------- RECARGA ------------------------------ #


class Ingrediente(db.Model):
    __tablename__ = "INGREDIENTES"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100), nullable=True)
