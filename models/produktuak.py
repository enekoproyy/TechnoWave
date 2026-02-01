from models import db

class Kategoriak(db.Model):
    """Modelo de categorías de productos"""
    
    __tablename__ = 'kategoriak'
    
    kategoria_id = db.Column(db.Integer, primary_key=True)
    izena = db.Column(db.String(100), nullable=False, unique=True)
    deskribapena = db.Column(db.Text)
    
    # Relaciones
    produktuak = db.relationship('Produktuak', backref='kategoria', lazy=True)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'kategoria_id': self.kategoria_id,
            'izena': self.izena,
            'deskribapena': self.deskribapena
        }


class Produktuak(db.Model):
    """Modelo de productos (produktuak)"""
    
    __tablename__ = 'produktuak'
    
    produktu_id = db.Column(db.Integer, primary_key=True)
    izena = db.Column(db.String(200), nullable=False)
    deskribapena = db.Column(db.Text)
    prezioa = db.Column(db.Float, nullable=False)
    irudi_urla = db.Column(db.String(300))
    kategoria_id = db.Column(db.Integer, db.ForeignKey('kategoriak.kategoria_id'), nullable=False)
    
    # Relaciones
    saski_elementuak = db.relationship('SaskiElementuak', backref='produktua', lazy=True)
    eskaera_elementuak = db.relationship('EskaeraElementuak', backref='produktua', lazy=True)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'produktu_id': self.produktu_id,
            'izena': self.izena,
            'deskribapena': self.deskribapena,
            'prezioa': self.prezioa,
            'irudi_urla': self.irudi_urla,
            'kategoria_id': self.kategoria_id,
            'kategoria_izena': self.kategoria.izena if self.kategoria else None
        }
