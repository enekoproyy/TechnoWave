from flask import render_template, request, jsonify, flash, redirect, url_for
from routes import produktuak_bp
from models import db
from models.produktuak import Produktuak, Kategoriak
from utils.auth import login_required

@produktuak_bp.route('/')
def index():
    """Muestra el catálogo de productos"""
    kategoria_id = request.args.get('kategoria_id', type=int)
    
    # Obtener todas las categorías
    kategoriak = Kategoriak.query.all()
    
    # Filtrar productos por categoría si se especifica
    if kategoria_id:
        produktuak = Produktuak.query.filter_by(kategoria_id=kategoria_id).all()
    else:
        produktuak = Produktuak.query.all()
    
    return render_template('produktuak.html', 
                         produktuak=produktuak, 
                         kategoriak=kategoriak,
                         selected_kategoria=kategoria_id)


@produktuak_bp.route('/<int:produktu_id>')
def detail(produktu_id):
    """Detalle de un producto"""
    produktua = Produktuak.query.get_or_404(produktu_id)
    return render_template('produktu_detail.html', produktua=produktua)


@produktuak_bp.route('/api/list')
def api_list():
    """API para listar productos (con filtros opcionales)"""
    kategoria_id = request.args.get('kategoria_id', type=int)
    
    query = Produktuak.query
    
    if kategoria_id:
        query = query.filter_by(kategoria_id=kategoria_id)
    
    produktuak = query.all()
    
    return jsonify({
        'success': True,
        'produktuak': [p.to_dict() for p in produktuak]
    })


@produktuak_bp.route('/kategoriak')
def kategoriak_list():
    """Lista de categorías"""
    kategoriak = Kategoriak.query.all()
    return jsonify({
        'success': True,
        'kategoriak': [k.to_dict() for k in kategoriak]
    })
