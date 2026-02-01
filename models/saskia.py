from models import db

class SaskiElementuak(db.Model):
    """
    Modelo del carrito de compra (saskia) - TEMPORAL
    El carrito es editable y usa precios dinámicos del catálogo actual
    """
    
    __tablename__ = 'saski_elementuak'
    
    erabiltzaile_id = db.Column(db.Integer, db.ForeignKey('erabiltzaileak.erabiltzaile_id'), primary_key=True)
    produktu_id = db.Column(db.Integer, db.ForeignKey('produktuak.produktu_id'), primary_key=True)
    kantitatea = db.Column(db.Integer, nullable=False, default=1)
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario.
        IMPORTANTE: El precio siempre se obtiene del catálogo actual.
        """
        return {
            'erabiltzaile_id': self.erabiltzaile_id,
            'produktu_id': self.produktu_id,
            'kantitatea': self.kantitatea,
            'produktu_izena': self.produktua.izena if self.produktua else None,
            'prezioa': self.produktua.prezioa if self.produktua else 0,  # Precio actual
            'subtotala': (self.produktua.prezioa * self.kantitatea) if self.produktua else 0,
            'irudi_urla': self.produktua.irudi_urla if self.produktua else None
        }
    
    @staticmethod
    def get_total(erabiltzaile_id):
        """Calcula el total del carrito usando precios actuales del catálogo"""
        items = SaskiElementuak.query.filter_by(erabiltzaile_id=erabiltzaile_id).all()
        total = sum(item.produktua.prezioa * item.kantitatea for item in items if item.produktua)
        return round(total, 2)
