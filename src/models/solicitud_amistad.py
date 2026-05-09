from database import db
from datetime import datetime

# ------------------------- SolicitudAmistad ------------------------ #


class SolicitudAmistad(db.Model):
    __tablename__ = "SOLICITUDES_AMISTAD"

    id = db.Column(db.Integer, primary_key=True)

    # Usuario que envía la solicitud
    id_remitente = db.Column(db.Integer, db.ForeignKey("USUARIOS.id"), nullable=False)
    # Usuario que recibe la solicitud
    id_receptor = db.Column(db.Integer, db.ForeignKey("USUARIOS.id"), nullable=False)

    # Fecha de creación de la solicitud
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones con Usuario
    remitente = db.relationship(
        "Usuario",
        foreign_keys=[id_remitente],
        backref=db.backref("solicitudes_enviadas", cascade="all, delete-orphan"),
    )

    receptor = db.relationship(
        "Usuario",
        foreign_keys=[id_receptor],
        backref=db.backref("solicitudes_recibidas", cascade="all, delete-orphan"),
    )

    def __init__(self, id_remitente, id_receptor):
        self.id_remitente = id_remitente
        self.id_receptor = id_receptor

    def __repr__(self):
        return f"<SolicitudAmistad id={self.id} remitente={self.id_remitente} receptor={self.id_receptor}>"
