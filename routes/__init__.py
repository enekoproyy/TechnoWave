from flask import Blueprint

# Inicializar blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
produktuak_bp = Blueprint('produktuak', __name__, url_prefix='/produktuak')
saskia_bp = Blueprint('saskia', __name__, url_prefix='/api/saskia')
eskaerak_bp = Blueprint('eskaerak', __name__, url_prefix='/api/eskaerak')

# Importar las rutas
from routes import auth, produktuak, saskia, eskaerak
