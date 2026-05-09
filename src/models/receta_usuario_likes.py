from database import db

# ---------------------------- Receta_Usuario_Likes ------------------------------ #


class Receta_Usuario_Likes(db.Model):
    __tablename__ = "RECETAS_USUARIOS_LIKES"

    id = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(
        db.Integer, db.ForeignKey("RECETAS.id", ondelete="CASCADE"), nullable=False
    )
    id_usuario = db.Column(
        db.Integer, db.ForeignKey("USUARIOS.id", ondelete="CASCADE"), nullable=False
    )

    receta = db.relationship(
        "Receta",
        backref=db.backref("usuarios_que_le_gustan", cascade="all, delete-orphan"),
    )

    usuario = db.relationship(
        "Usuario",
        backref=db.backref("recetas_que_le_gustan", cascade="all, delete-orphan"),
    )

    def __init__(self, id_receta, id_usuario):
        self.id_receta = id_receta
        self.id_usuario = id_usuario

    def __repr__(self):
        return f"<Receta_Usuario_Likes id={self.id} id_receta={self.id_receta} id_usuario={self.id_usuario}>"
