from database import db

# ---------------------------- USUARIO ------------------------------ #


class Usuario(db.Model):
    __tablename__ = "USUARIOS"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(75), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String, nullable=False)
    gmail = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(75), nullable=True)
    foto = db.Column(db.String(255), nullable=True)

    def __init__(
        self, nombre, apellidos, usuario, contrasena, gmail, descripcion=None, foto=None
    ):
        self.nombre = nombre
        self.apellidos = apellidos
        self.usuario = usuario
        self.contrasena = contrasena
        self.gmail = gmail
        self.descripcion = descripcion
        self.foto = foto

    def __repr__(self):
        return f"<Usuario id={self.id} usuario={self.usuario!r}>"
