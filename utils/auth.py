from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'erabiltzaile_id' not in session:
            flash('Mesedez, hasi saioa jarraitzeko / Por favor, inicia sesión para continuar', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    from models.erabiltzaileak import Erabiltzaileak
    
    if 'erabiltzaile_id' in session:
        return Erabiltzaileak.query.get(session['erabiltzaile_id'])
    return None
