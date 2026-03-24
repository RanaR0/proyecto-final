from database import db

# ---------------------------- Amigo ------------------------------ #


class Amigo(db.Model):
    __tablename__ = "AMIGOS"

    id = db.Column(db.Integer, primary_key=True)

    # 1. Definir que son llaves foráneas apuntando a la tabla usuarios
    id_usuario = db.Column(db.Integer, db.ForeignKey('USUARIOS.id'), nullable=False)
    id_amigo = db.Column(db.Integer, db.ForeignKey('USUARIOS.id'), nullable=False)

    # 2. Especificar explícitamente qué columna usar para cada relación
    usuario = db.relationship(
        "Usuario",
        foreign_keys=[id_usuario],
        backref=db.backref("amigos_asociados", cascade="all, delete-orphan")
    )

    amigo = db.relationship(
        "Usuario",
        foreign_keys=[id_amigo],
        backref=db.backref("amigos_de", cascade="all, delete-orphan")
    )