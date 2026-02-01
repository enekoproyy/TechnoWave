from flask import Flask, render_template
from config import Config
from models import db
from routes import auth_bp, produktuak_bp, saskia_bp, eskaerak_bp

def create_app(config_class=Config):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(produktuak_bp)
    app.register_blueprint(saskia_bp)
    app.register_blueprint(eskaerak_bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Ruta para ver el carrito
    @app.route('/saskia')
    def saskia_view():
        return render_template('saskia.html')
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
