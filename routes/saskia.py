from flask import request, jsonify, session
from routes import saskia_bp
from models import db
from models.saskia import SaskiElementuak
from models.produktuak import Produktuak
from utils.auth import login_required

@saskia_bp.route('/gehitu', methods=['POST'])
@login_required
def gehitu():
    """
    Añadir producto al carrito (saskia)
    El carrito es TEMPORAL y EDITABLE
    """
    data = request.get_json()
    produktu_id = data.get('produktu_id')
    kantitatea = data.get('kantitatea', 1)
    
    if not produktu_id:
        return jsonify({'success': False, 'message': 'produktu_id beharrezkoa da'}), 400
    
    # Verificar que el producto existe
    produktua = Produktuak.query.get(produktu_id)
    if not produktua:
        return jsonify({'success': False, 'message': 'Produktua ez da existitzen'}), 404
    
    erabiltzaile_id = session['erabiltzaile_id']
    
    # Verificar si el producto ya está en el carrito
    item = SaskiElementuak.query.filter_by(
        erabiltzaile_id=erabiltzaile_id,
        produktu_id=produktu_id
    ).first()
    
    try:
        if item:
            # Actualizar cantidad
            item.kantitatea += kantitatea
        else:
            # Crear nuevo item
            item = SaskiElementuak(
                erabiltzaile_id=erabiltzaile_id,
                produktu_id=produktu_id,
                kantitatea=kantitatea
            )
            db.session.add(item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produktua saskira gehitu da / Producto añadido al carrito',
            'item': item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@saskia_bp.route('/ikusi', methods=['GET'])
@login_required
def ikusi():
    """
    Ver el carrito completo
    IMPORTANTE: Los precios se calculan dinámicamente del catálogo actual
    """
    erabiltzaile_id = session['erabiltzaile_id']
    
    items = SaskiElementuak.query.filter_by(erabiltzaile_id=erabiltzaile_id).all()
    
    total = SaskiElementuak.get_total(erabiltzaile_id)
    
    return jsonify({
        'success': True,
        'items': [item.to_dict() for item in items],
        'totala': total
    })


@saskia_bp.route('/eguneratu', methods=['PUT'])
@login_required
def eguneratu():
    """
    Actualizar cantidad de un producto en el carrito
    El carrito es EDITABLE
    """
    data = request.get_json()
    produktu_id = data.get('produktu_id')
    kantitatea = data.get('kantitatea', 1)
    
    if not produktu_id:
        return jsonify({'success': False, 'message': 'produktu_id beharrezkoa da'}), 400
    
    if kantitatea < 1:
        return jsonify({'success': False, 'message': 'Kantitatea 1 baino handiagoa izan behar da'}), 400
    
    erabiltzaile_id = session['erabiltzaile_id']
    
    item = SaskiElementuak.query.filter_by(
        erabiltzaile_id=erabiltzaile_id,
        produktu_id=produktu_id
    ).first()
    
    if not item:
        return jsonify({'success': False, 'message': 'Elementua ez da aurkitu saskian'}), 404
    
    try:
        item.kantitatea = kantitatea
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Kantitatea eguneratuta / Cantidad actualizada',
            'item': item.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@saskia_bp.route('/kendu', methods=['DELETE'])
@login_required
def kendu():
    """
    Eliminar producto del carrito
    El carrito es EDITABLE
    """
    data = request.get_json()
    produktu_id = data.get('produktu_id')
    
    if not produktu_id:
        return jsonify({'success': False, 'message': 'produktu_id beharrezkoa da'}), 400
    
    erabiltzaile_id = session['erabiltzaile_id']
    
    item = SaskiElementuak.query.filter_by(
        erabiltzaile_id=erabiltzaile_id,
        produktu_id=produktu_id
    ).first()
    
    if not item:
        return jsonify({'success': False, 'message': 'Elementua ez da aurkitu saskian'}), 404
    
    try:
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Produktua saskitik kenduta / Producto eliminado del carrito'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@saskia_bp.route('/hustu', methods=['DELETE'])
@login_required
def hustu():
    """Vaciar todo el carrito"""
    erabiltzaile_id = session['erabiltzaile_id']
    
    try:
        SaskiElementuak.query.filter_by(erabiltzaile_id=erabiltzaile_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Saskia hustuta / Carrito vaciado'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
