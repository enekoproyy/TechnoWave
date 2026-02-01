import os

class Config:
    """Configuración de la aplicación Flask"""
    
    # Clave secreta para sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de la base de datos
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'technowave.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesión
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
