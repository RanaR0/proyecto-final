from database import db

# ---------------------------- USUARIO ------------------------------ #


class Usuario(db.Model):
    __tablename__ = "USUARIOS"

    num_paso = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey("RECETAS.id", ondelete="CASCADE"), nullable=False)
    texto = db.Column(db.String(500), nullable=False)

