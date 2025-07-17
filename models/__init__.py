# Archivo: models/__init__.py

from app import db

# Tabla para los roles de usuario (Admin, Manager, Employer)
class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    # Relación con la tabla de usuarios
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

# Tabla para los grupos de Manager
class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    # Relación con la tabla de usuarios (Managers)
    usuarios = db.relationship('Usuario', backref='grupo', lazy=True)

# Tabla para los usuarios del sistema
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'
    
# Archivo: models/__init__.py

from app import db

# (Código anterior para Rol, Grupo, Usuario...)

# Importa los nuevos modelos de los informes para que sean reconocidos por SQLAlchemy
from .informes import Informe, SeccionInforme
from .monitoreo import Monitoreo, DetalleCorreoAtacante
from .vulnerabilidades import Vulnerabilidad
from .incidentes import Incidente, CadenaLlamada