from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos los modelos
from models.erabiltzaileak import Erabiltzaileak
from models.produktuak import Kategoriak, Produktuak
from models.saskia import SaskiElementuak
from models.eskaerak import Eskaerak, EskaeraElementuak
