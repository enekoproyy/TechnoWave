from models import db
from datetime import datetime

class Eskaerak(db.Model):
    """
    Modelo de pedidos (eskaerak) - PERMANENTE
    Los pedidos NO son editables una vez creados
    """
    
    __tablename__ = 'eskaerak'
    
    eskaera_id = db.Column(db.Integer, primary_key=True)
    erabiltzaile_id = db.Column(db.Integer, db.ForeignKey('erabiltzaileak.erabiltzaile_id'), nullable=False)
    sormen_data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    egoera = db.Column(db.String(50), nullable=False, default='Ordainduta')
    # Estados válidos: Ordainduta, Prestatzen, Bidean, Entregatuta
    
    # Relaciones
    eskaera_elementuak = db.relationship('EskaeraElementuak', backref='eskaera', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        items = [item.to_dict() for item in self.eskaera_elementuak]
        total = sum(item.prezioa * item.kantitatea for item in self.eskaera_elementuak)
        
        return {
            'eskaera_id': self.eskaera_id,
            'erabiltzaile_id': self.erabiltzaile_id,
            'sormen_data': self.sormen_data.isoformat() if self.sormen_data else None,
            'egoera': self.egoera,
            'elementuak': items,
            'totala': round(total, 2)
        }


class EskaeraElementuak(db.Model):
    """
    Modelo de elementos del pedido - PERMANENTE
    IMPORTANTE: Guarda el precio histórico en el momento de la compra
    """
    
    __tablename__ = 'eskaera_elementuak'
    
    eskaera_id = db.Column(db.Integer, db.ForeignKey('eskaerak.eskaera_id'), primary_key=True)
    produktu_id = db.Column(db.Integer, db.ForeignKey('produktuak.produktu_id'), primary_key=True)
    kantitatea = db.Column(db.Integer, nullable=False)
    prezioa = db.Column(db.Float, nullable=False)  # PRECIO HISTÓRICO guardado al momento de compra
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'eskaera_id': self.eskaera_id,
            'produktu_id': self.produktu_id,
            'kantitatea': self.kantitatea,
            'prezioa': self.prezioa,  # Precio histórico
            'subtotala': round(self.prezioa * self.kantitatea, 2),
            'produktu_izena': self.produktua.izena if self.produktua else 'Producto eliminado'
        }
