from flask import request, jsonify, session, render_template
from routes import eskaerak_bp
from models import db
from models.eskaerak import Eskaerak, EskaeraElementuak
from models.saskia import SaskiElementuak
from utils.auth import login_required
from datetime import datetime

@eskaerak_bp.route('/sortu', methods=['POST'])
@login_required
def sortu():
    """
    Crear pedido desde el carrito
    LÓGICA CRÍTICA:
    1. Copiar productos del carrito a eskaera_elementuak
    2. Guardar PRECIO HISTÓRICO (precio actual del catálogo)
    3. Vaciar el carrito
    4. El pedido es PERMANENTE y NO EDITABLE
    """
    erabiltzaile_id = session['erabiltzaile_id']
    
    # Obtener items del carrito
    saski_items = SaskiElementuak.query.filter_by(erabiltzaile_id=erabiltzaile_id).all()
    
    if not saski_items:
        return jsonify({
            'success': False,
            'message': 'Saskia hutsik dago / El carrito está vacío'
        }), 400
    
    try:
        # Crear nuevo pedido
        eskaera = Eskaerak(
            erabiltzaile_id=erabiltzaile_id,
            sormen_data=datetime.utcnow(),
            egoera='Ordainduta'
        )
        db.session.add(eskaera)
        db.session.flush()  # Para obtener el eskaera_id
        
        # Copiar items del carrito al pedido con PRECIO HISTÓRICO
        for item in saski_items:
            # IMPORTANTE: Guardar el precio actual del catálogo como precio histórico
            eskaera_item = EskaeraElementuak(
                eskaera_id=eskaera.eskaera_id,
                produktu_id=item.produktu_id,
                kantitatea=item.kantitatea,
                prezioa=item.produktua.prezioa  # PRECIO HISTÓRICO guardado
            )
            db.session.add(eskaera_item)
        
        # Vaciar el carrito
        SaskiElementuak.query.filter_by(erabiltzaile_id=erabiltzaile_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Eskaera arrakastaz sortuta / Pedido creado con éxito',
            'eskaera': eskaera.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Errorea eskaera sortzean / Error al crear pedido: {str(e)}'
        }), 500


@eskaerak_bp.route('/zerrenda', methods=['GET'])
@login_required
def zerrenda():
    """Listar todos los pedidos del usuario"""
    erabiltzaile_id = session['erabiltzaile_id']
    
    eskaerak = Eskaerak.query.filter_by(erabiltzaile_id=erabiltzaile_id)\
        .order_by(Eskaerak.sormen_data.desc()).all()
    
    return jsonify({
        'success': True,
        'eskaerak': [eskaera.to_dict() for eskaera in eskaerak]
    })


@eskaerak_bp.route('/<int:eskaera_id>', methods=['GET'])
@login_required
def ikusi(eskaera_id):
    """Ver detalle de un pedido específico"""
    erabiltzaile_id = session['erabiltzaile_id']
    
    eskaera = Eskaerak.query.filter_by(
        eskaera_id=eskaera_id,
        erabiltzaile_id=erabiltzaile_id
    ).first()
    
    if not eskaera:
        return jsonify({
            'success': False,
            'message': 'Eskaera ez da aurkitu / Pedido no encontrado'
        }), 404
    
    return jsonify({
        'success': True,
        'eskaera': eskaera.to_dict()
    })


@eskaerak_bp.route('/egoera/<int:eskaera_id>', methods=['PUT'])
@login_required
def eguneratu_egoera(eskaera_id):
    """
    Actualizar el estado de un pedido
    Estados válidos: Ordainduta, Prestatzen, Bidean, Entregatuta
    NOTA: Los productos del pedido NO se pueden modificar
    """
    data = request.get_json()
    egoera_berria = data.get('egoera')
    
    # Validar estados
    egoera_baliodunak = ['Ordainduta', 'Prestatzen', 'Bidean', 'Entregatuta']
    if egoera_berria not in egoera_baliodunak:
        return jsonify({
            'success': False,
            'message': f'Egoera ez da baliozkoa. Baliozko egoerak: {", ".join(egoera_baliodunak)}'
        }), 400
    
    erabiltzaile_id = session['erabiltzaile_id']
    
    eskaera = Eskaerak.query.filter_by(
        eskaera_id=eskaera_id,
        erabiltzaile_id=erabiltzaile_id
    ).first()
    
    if not eskaera:
        return jsonify({
            'success': False,
            'message': 'Eskaera ez da aurkitu / Pedido no encontrado'
        }), 404
    
    try:
        eskaera.egoera = egoera_berria
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Egoera eguneratuta / Estado actualizado',
            'eskaera': eskaera.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@eskaerak_bp.route('/view')
@login_required
def view_eskaerak():
    """Vista HTML de pedidos"""
    return render_template('eskaerak.html')
