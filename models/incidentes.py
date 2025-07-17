from app import db
from .informes import Informe

# Tabla para el detalle de los incidentes (del informe de incidentes)
class Incidente(db.Model):
    __tablename__ = 'incidentes'
    id = db.Column(db.Integer, primary_key=True)
    informe_id = db.Column(db.Integer, db.ForeignKey('informes.id'), nullable=False)
    fecha_apertura = db.Column(db.DateTime, nullable=False)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    asunto = db.Column(db.String(255), nullable=False)
    origen = db.Column(db.String(100), nullable=False)
    detalles = db.Column(db.Text, nullable=False)
    acciones_tomadas = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum('ABIERTO', 'CERRADO', 'EN PROCESO', name='estado_incidente_enum'), nullable=False)
    criticidad = db.Column(db.Enum('Baja', 'Media', 'Alta', 'Crítica', name='criticidad_incidente_enum'), nullable=False)
    prioridad = db.Column(db.String(50), nullable=False)
    sitio_afectado = db.Column(db.String(255), nullable=True)
    ip_origen = db.Column(db.String(50), nullable=True)
    usuario_responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    analista_responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    informe = db.relationship('Informe', backref='detalles_incidente')
    usuario_responsable = db.relationship('Usuario', foreign_keys=[usuario_responsable_id])
    analista_responsable = db.relationship('Usuario', foreign_keys=[analista_responsable_id])

# Tabla para la cadena de llamadas del incidente
class CadenaLlamada(db.Model):
    __tablename__ = 'cadena_llamadas'
    id = db.Column(db.Integer, primary_key=True)
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    persona_contacto = db.Column(db.String(150), nullable=False)
    area_contacto = db.Column(db.String(150), nullable=False)
    accion_comunicacion = db.Column(db.String(100), nullable=False)
    detalles_comunicacion = db.Column(db.Text, nullable=False)
    
    incidente = db.relationship('Incidente', backref='cadena_comunicacion')