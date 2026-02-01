#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de ejemplo
"""
from app import create_app
from models import db
from models.produktuak import Kategoriak, Produktuak

def init_db():
    """Inicializa la base de datos con datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        # Eliminar todas las tablas existentes y recrearlas
        print("Inicializando base de datos...")
        db.drop_all()
        db.create_all()
        
        # Crear categorías
        kategoriak = [
            Kategoriak(izena='Ordenagailuak / Ordenadores', deskribapena='Ordenadores portátiles y de sobremesa'),
            Kategoriak(izena='Telefonoak / Teléfonos', deskribapena='Smartphones y teléfonos móviles'),
            Kategoriak(izena='Tabletoak / Tablets', deskribapena='Tablets y dispositivos táctiles'),
            Kategoriak(izena='Osagarriak / Accesorios', deskribapena='Accesorios y periféricos'),
        ]
        
        for kategoria in kategoriak:
            db.session.add(kategoria)
        
        db.session.commit()
        print(f"✓ {len(kategoriak)} kategoría(s) creada(s)")
        
        # Crear productos de ejemplo
        produktuak = [
            # Ordenadores
            Produktuak(
                izena='MacBook Pro 14"',
                deskribapena='Portátil profesional con chip M3 Pro, 16GB RAM, 512GB SSD',
                prezioa=2499.99,
                irudi_urla='static/img/macbook.jpg',
                kategoria_id=1
            ),
            Produktuak(
                izena='Dell XPS 13',
                deskribapena='Ultrabook compacto con Intel i7, 16GB RAM, 512GB SSD',
                prezioa=1399.99,
                irudi_urla='static/img/dellxps13.jpg',
                kategoria_id=1
            ),
            Produktuak(
                izena='HP Pavilion Gaming',
                deskribapena='Portátil gaming con RTX 4060, 16GB RAM, 1TB SSD',
                prezioa=1199.99,
                irudi_urla='static/img/hppavilon.jfif',
                kategoria_id=1
            ),
            
            # Teléfonos
            Produktuak(
                izena='iPhone 15 Pro',
                deskribapena='Smartphone con chip A17 Pro, 256GB, cámara 48MP',
                prezioa=1199.99,
                irudi_urla='static/img/iphone15.jpg',
                kategoria_id=2
            ),
            Produktuak(
                izena='Samsung Galaxy S24',
                deskribapena='Smartphone Android con Snapdragon 8 Gen 3, 256GB',
                prezioa=999.99,
                irudi_urla='static/img/samsunggalaxys24.jpg',
                kategoria_id=2
            ),
            Produktuak(
                izena='Google Pixel 8',
                deskribapena='Smartphone con Google Tensor G3, 128GB, Android puro',
                prezioa=699.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?google,pixel,phone',
                kategoria_id=2
            ),
            
            # Tablets
            Produktuak(
                izena='iPad Air',
                deskribapena='Tablet con chip M2, 128GB, pantalla Liquid Retina 11"',
                prezioa=699.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?ipad,tablet',
                kategoria_id=3
            ),
            Produktuak(
                izena='Samsung Galaxy Tab S9',
                deskribapena='Tablet Android premium con S Pen, 256GB, 11"',
                prezioa=599.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?tablet,android',
                kategoria_id=3
            ),
            
            # Accesorios
            Produktuak(
                izena='AirPods Pro 2',
                deskribapena='Auriculares inalámbricos con cancelación de ruido activa',
                prezioa=279.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?earbuds,headphones',
                kategoria_id=4
            ),
            Produktuak(
                izena='Logitech MX Master 3S',
                deskribapena='Ratón inalámbrico ergonómico profesional',
                prezioa=109.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?mouse,peripheral',
                kategoria_id=4
            ),
            Produktuak(
                izena='Apple Magic Keyboard',
                deskribapena='Teclado inalámbrico compacto con batería recargable',
                prezioa=129.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?keyboard,apple',
                kategoria_id=4
            ),
            Produktuak(
                izena='SanDisk Extreme Pro 1TB',
                deskribapena='SSD externo portátil, velocidad hasta 2000MB/s',
                prezioa=159.99,
                irudi_urla='https://source.unsplash.com/featured/600x400?ssd,external,drive',
                kategoria_id=4
            ),
        ]
        
        for produktua in produktuak:
            db.session.add(produktua)
        
        db.session.commit()
        print(f"✓ {len(produktuak)} producto(s) creado(s)")
        
        print("\n" + "="*50)
        print("✓ Base de datos inicializada correctamente")
        print("="*50)
        print("\nCategorías creadas:")
        for kat in kategoriak:
            print(f"  - {kat.izena}")
        print(f"\nTotal productos: {len(produktuak)}")
        print("\n¡La aplicación está lista para usar!")
        print("Ejecuta: python app.py")

if __name__ == '__main__':
    init_db()
