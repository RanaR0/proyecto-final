from database import db

# ---------------------------- Amigo ------------------------------ #


class Amigo(db.Model):
    __tablename__ = "AMIGOS"

    id = db.Column(db.Integer, primary_key=True)

    # 1. Definir que son llaves foráneas apuntando a la tabla usuarios
    id_usuario = db.Column(db.Integer, db.ForeignKey("USUARIOS.id"), nullable=False)
    id_amigo = db.Column(db.Integer, db.ForeignKey("USUARIOS.id"), nullable=False)

    # 3. Estado de la amistad (si fue aceptada o aún está pendiente)
    aceptado = db.Column(db.Boolean, default=False, nullable=False)

    # 2. Especificar explícitamente qué columna usar para cada relación
    usuario = db.relationship(
        "Usuario",
        foreign_keys=[id_usuario],
        backref=db.backref("amigos_asociados", cascade="all, delete-orphan"),
    )

    amigo = db.relationship(
        "Usuario",
        foreign_keys=[id_amigo],
        backref=db.backref("amigos_de", cascade="all, delete-orphan"),
    )

    def __init__(self, id_usuario, id_amigo, aceptado=False):
        self.id_usuario = id_usuario
        self.id_amigo = id_amigo
        self.aceptado = aceptado

    def __repr__(self):
        return f"<Amigo id={self.id} id_usuario={self.id_usuario} id_amigo={self.id_amigo} aceptado={self.aceptado}>"
