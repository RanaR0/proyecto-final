from database import db

# ---------------------------- Seguidor ------------------------------ #


class Seguidor(db.Model):
    __tablename__ = "SEGUIDORES"

    id = db.Column(db.Integer, primary_key=True)

    id_seguidor = db.Column(db.Integer, db.ForeignKey("USUARIOS.id"), nullable=False)
    id_seguido = db.Column(db.Integer, db.ForeignKey("USUARIOS.id"), nullable=False)

    seguidor = db.relationship(
        "Usuario",
        foreign_keys=[id_seguidor],
        backref=db.backref("seguidores_asociados", cascade="all, delete-orphan"),
    )

    seguido = db.relationship(
        "Usuario",
        foreign_keys=[id_seguido],
        backref=db.backref("seguidos_asociados", cascade="all, delete-orphan"),
    )

    def __init__(self, id_seguidor, id_seguido):
        self.id_seguidor = id_seguidor
        self.id_seguido = id_seguido

    def __repr__(self):
        return f"<Seguidor: {self.id_seguidor} sigue a {self.id_seguido}>"
