# Archivo: models/__init__.py

from app import db, bcrypt
from .informes import Informe, SeccionInforme
from .monitoreo import Monitoreo, DetalleCorreoAtacante
from .vulnerabilidades import Vulnerabilidad
from .incidentes import Incidente, CadenaLlamada

# Tabla para los roles de usuario (Admin, Manager, Employer)
class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    # Relación con la tabla de usuarios
    usuarios = db.relationship('Usuario', backref='rol_usuario', lazy=True)

# Tabla para los grupos de Manager
class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    # Relación con la tabla de usuarios (Managers)
    usuarios = db.relationship('Usuario', backref='grupo_usuario', lazy=True)

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

    # Relaciones para poder acceder al rol y al grupo
    rol = db.relationship('Rol', backref='usuarios_por_rol', foreign_keys=[rol_id])
    grupo = db.relationship('Grupo', backref='usuarios_por_grupo', foreign_keys=[grupo_id])

    # Método para hashear la contraseña
    def set_password(self, password):
        self.contrasena_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Método para verificar la contraseña
    def check_password(self, password):
        return bcrypt.check_password_hash(self.contrasena_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'