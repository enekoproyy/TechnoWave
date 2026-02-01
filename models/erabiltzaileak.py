from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Erabiltzaileak(db.Model):
    """Modelo de usuarios (erabiltzaileak)"""
    
    __tablename__ = 'erabiltzaileak'
    
    erabiltzaile_id = db.Column(db.Integer, primary_key=True)
    helbide_elektronikoa = db.Column(db.String(120), unique=True, nullable=False, index=True)
    pasahitza = db.Column(db.String(255), nullable=False)
    izena = db.Column(db.String(100), nullable=False)
    abizenak = db.Column(db.String(100), nullable=False)
    tfnoa = db.Column(db.String(20))
    sormen_data = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    saski_elementuak = db.relationship('SaskiElementuak', backref='erabiltzailea', lazy=True, cascade='all, delete-orphan')
    eskaerak = db.relationship('Eskaerak', backref='erabiltzailea', lazy=True)
    
    def set_password(self, password):
        """Genera hash seguro de la contraseña"""
        self.pasahitza = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.pasahitza, password)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'erabiltzaile_id': self.erabiltzaile_id,
            'helbide_elektronikoa': self.helbide_elektronikoa,
            'izena': self.izena,
            'abizenak': self.abizenak,
            'tfnoa': self.tfnoa,
            'sormen_data': self.sormen_data.isoformat() if self.sormen_data else None
        }
