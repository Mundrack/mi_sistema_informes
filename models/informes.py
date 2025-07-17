from app import db
import datetime

# Tabla para los Informes
class Informe(db.Model):
    __tablename__ = 'informes'
    id = db.Column(db.Integer, primary_key=True)
    report_number = db.Column(db.String(50), nullable=True) # Del informe de vulnerabilidades
    titulo = db.Column(db.String(255), nullable=False)
    asunto = db.Column(db.String(255), nullable=True)
    destinatario = db.Column(db.String(150), nullable=True)
    tipo_informe = db.Column(db.Enum('monitoreo', 'boletin', 'vulnerabilidad', 'incidente', name='tipo_informe_enum'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    estado_eliminado = db.Column(db.Boolean, default=False)
    
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)

# Tabla para el Contenido del Informe (para boletines y secciones de texto)
class SeccionInforme(db.Model):
    __tablename__ = 'secciones_informe'
    id = db.Column(db.Integer, primary_key=True)
    informe_id = db.Column(db.Integer, db.ForeignKey('informes.id'), nullable=False)
    seccion_titulo = db.Column(db.String(150), nullable=True)
    contenido_html = db.Column(db.Text, nullable=True)