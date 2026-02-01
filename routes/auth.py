from flask import render_template, request, redirect, url_for, flash, session
from routes import auth_bp
from models import db
from models.erabiltzaileak import Erabiltzaileak
import re

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        helbide_elektronikoa = request.form.get('helbide_elektronikoa', '').strip()
        pasahitza = request.form.get('pasahitza', '')
        pasahitza_confirm = request.form.get('pasahitza_confirm', '')
        izena = request.form.get('izena', '').strip()
        abizenak = request.form.get('abizenak', '').strip()
        tfnoa = request.form.get('tfnoa', '').strip()
        
        # Validaciones
        errors = []
        
        if not helbide_elektronikoa or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', helbide_elektronikoa):
            errors.append('Email baliozkoa behar da / Email válido requerido')
        
        if not pasahitza or len(pasahitza) < 6:
            errors.append('Pasahitzak gutxienez 6 karaktere izan behar ditu / La contraseña debe tener al menos 6 caracteres')
        
        if pasahitza != pasahitza_confirm:
            errors.append('Pasahitzak ez datoz bat / Las contraseñas no coinciden')
        
        if not izena:
            errors.append('Izena beharrezkoa da / Nombre requerido')
        
        if not abizenak:
            errors.append('Abizenak beharrezkoak dira / Apellidos requeridos')
        
        # Verificar si el email ya existe
        if Erabiltzaileak.query.filter_by(helbide_elektronikoa=helbide_elektronikoa).first():
            errors.append('Email hau erregistratuta dago / Este email ya está registrado')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        # Crear nuevo usuario
        try:
            erabiltzailea = Erabiltzaileak(
                helbide_elektronikoa=helbide_elektronikoa,
                izena=izena,
                abizenak=abizenak,
                tfnoa=tfnoa
            )
            erabiltzailea.set_password(pasahitza)
            
            db.session.add(erabiltzailea)
            db.session.commit()
            
            flash('Erregistroa arrakastatsua! Orain hasi saioa / ¡Registro exitoso! Ahora inicia sesión', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Errorea erregistroan / Error en el registro: {str(e)}', 'danger')
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if request.method == 'POST':
        helbide_elektronikoa = request.form.get('helbide_elektronikoa', '').strip()
        pasahitza = request.form.get('pasahitza', '')
        
        if not helbide_elektronikoa or not pasahitza:
            flash('Email eta pasahitza beharrezkoak dira / Email y contraseña requeridos', 'danger')
            return render_template('login.html')
        
        # Buscar usuario
        erabiltzailea = Erabiltzaileak.query.filter_by(helbide_elektronikoa=helbide_elektronikoa).first()
        
        if erabiltzailea and erabiltzailea.check_password(pasahitza):
            # Iniciar sesión
            session['erabiltzaile_id'] = erabiltzailea.erabiltzaile_id
            session['izena'] = erabiltzailea.izena
            session.permanent = True
            
            flash(f'Ongi etorri, {erabiltzailea.izena}! / ¡Bienvenido, {erabiltzailea.izena}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email edo pasahitz okerra / Email o contraseña incorrectos', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Saioa itxi da / Sesión cerrada', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/profile')
def profile():
    """Perfil de usuario"""
    from utils.auth import login_required, get_current_user
    
    @login_required
    def show_profile():
        erabiltzailea = get_current_user()
        return render_template('profile.html', erabiltzailea=erabiltzailea)
    
    return show_profile()
