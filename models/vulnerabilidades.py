from app import db
from .informes import Informe

# Tabla para el detalle de las vulnerabilidades (del informe de vulnerabilidades)
class Vulnerabilidad(db.Model):
    __tablename__ = 'vulnerabilidades'
    id = db.Column(db.Integer, primary_key=True)
    informe_id = db.Column(db.Integer, db.ForeignKey('informes.id'), nullable=False)
    nombre_vulnerabilidad = db.Column(db.String(255), nullable=False)
    nivel_criticidad = db.Column(db.Enum('Baja', 'Media', 'Alta', 'Crítica', name='criticidad_enum'), nullable=False)
    sitio_web = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    impacto = db.Column(db.Text, nullable=False)
    mitigacion = db.Column(db.Text, nullable=False)
    
    informe = db.relationship('Informe', backref='vulnerabilidades_list')