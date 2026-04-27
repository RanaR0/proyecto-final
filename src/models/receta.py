from database import db

# ---------------------------- Receta ------------------------------ #


class Receta(db.Model):
    __tablename__ = "RECETAS"  # Recomendado en plural para consistencia

    id = db.Column(db.Integer, primary_key=True)

    # Corregido el nombre de la tabla foránea (ajusta según tu clase Usuario)
    id_propietario = db.Column(
        db.Integer, db.ForeignKey("USUARIOS.id", ondelete="CASCADE"), nullable=False
    )

    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    # Eliminado unique=True para evitar errores al repetir descripciones o raciones
    descripcion = db.Column(db.String(500), nullable=False)
    tiempo = db.Column(db.Integer, nullable=False)
    raciones = db.Column(db.String(50), nullable=False)

    destacado = db.Column(db.Boolean, default=False)
    foto_principal = db.Column(db.String(255), nullable=True)

    # Columnas para el sistema de versioning
    version = db.Column(db.Integer, default=1)
    archivado = db.Column(db.Boolean, default=False)
    copia_de = db.Column(
        db.Integer, db.ForeignKey("RECETAS.id"), nullable=True
    )  # Si es una copia, referencia a la receta original
    usuario_original_id = db.Column(
        db.Integer, db.ForeignKey("USUARIOS.id"), nullable=True
    )  # Quién creó la receta original si es una copia
    creador_original = db.Column(
        db.String(50), nullable=True
    )  # @usuario del creador original para mostrar

    # Relación bidireccional con los Pasos
    pasos = db.relationship(
        "Paso", back_populates="receta", cascade="all, delete-orphan"
    )

    # Relaciones para el sistema de versioning
    receta_original = db.relationship(
        "Receta",
        remote_side=[id],
        foreign_keys=[copia_de],
        backref="copias",
        post_update=True,
    )

    usuario_original = db.relationship(
        "Usuario", foreign_keys=[usuario_original_id], backref="recetas_copiadas"
    )

    def __init__(
        self,
        id_propietario,
        nombre,
        tipo,
        categoria,
        descripcion,
        tiempo,
        raciones,
        destacado=False,
        foto_principal=None,
        version=1,
        archivado=False,
        copia_de=None,
        usuario_original_id=None,
        creador_original=None,
    ):
        self.id_propietario = id_propietario
        self.nombre = nombre
        self.tipo = tipo
        self.categoria = categoria
        self.descripcion = descripcion
        self.tiempo = tiempo
        self.raciones = raciones
        self.destacado = destacado
        self.foto_principal = foto_principal
        self.version = version
        self.archivado = archivado
        self.copia_de = copia_de
        self.usuario_original_id = usuario_original_id
        self.creador_original = creador_original

    # Puedes añadir un método __repr__ para ver mejor la receta en consola
    def __repr__(self):
        return f"<Receta {self.nombre}>"

    @property
    def ingredientes_lista(self):
        """Retorna una lista de nombres de ingredientes relacionados a esta receta."""
        from models.receta_ingrediente import Receta_Ingrediente

        rels = Receta_Ingrediente.query.filter_by(id_receta=self.id).all()
        return [rel.ingrediente.nombre for rel in rels if rel.ingrediente]

    @property
    def pasos_lista(self):
        """Retorna una lista de textos de pasos ordenados por número de paso."""
        return [paso.texto for paso in sorted(self.pasos, key=lambda p: p.num_paso)]

    @property
    def pasos_con_fotos(self):
        """Retorna una lista de pasos con sus fotos asociadas."""
        return sorted(self.pasos, key=lambda p: p.num_paso)
