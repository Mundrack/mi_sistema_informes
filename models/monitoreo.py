from app import db
from .informes import Informe

# Tabla para el detalle de los informes de Monitoreo
class Monitoreo(db.Model):
    __tablename__ = 'monitoreo'
    id = db.Column(db.Integer, primary_key=True)
    informe_id = db.Column(db.Integer, db.ForeignKey('informes.id'), nullable=False)
    tipo_amenaza = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    
    informe = db.relationship('Informe', backref='detalles_monitoreo')

# Tabla para los detalles de correos atacantes (del informe de monitoreo)
class DetalleCorreoAtacante(db.Model):
    __tablename__ = 'detalle_correo_atacante'
    id = db.Column(db.Integer, primary_key=True)
    informe_id = db.Column(db.Integer, db.ForeignKey('informes.id'), nullable=False)
    correo_atacante = db.Column(db.String(255), nullable=False)
    dominio_afectado = db.Column(db.String(255), nullable=False)
    acciones_tomadas = db.Column(db.Text, nullable=False)
    
    informe = db.relationship('Informe', backref='correos_atacantes')