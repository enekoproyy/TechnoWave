"""
GUÍA DE USO - TechnoWave
========================

La aplicación está corriendo en: http://localhost:5000

FLUJO DE USO COMPLETO:
======================

1. REGISTRO DE USUARIO
   - Ir a: http://localhost:5000/auth/register
   - Completar el formulario con:
     * Email válido
     * Contraseña (mínimo 6 caracteres)
     * Nombre y apellidos
     * Teléfono (opcional)
   - Hacer clic en "Erregistratu / Registrarse"

2. INICIAR SESIÓN
   - Ir a: http://localhost:5000/auth/login
   - Ingresar email y contraseña
   - Hacer clic en "Hasi saioa / Login"

3. NAVEGAR POR EL CATÁLOGO
   - Ir a: http://localhost:5000/produktuak
   - Ver productos organizados por categorías:
     * Ordenagailuak / Ordenadores
     * Telefonoak / Teléfonos
     * Tabletoak / Tablets
     * Osagarriak / Accesorios
   - Filtrar por categoría haciendo clic en los botones superiores

4. AÑADIR AL CARRITO
   - En cada producto, hacer clic en "Saskira gehitu / Añadir al carrito"
   - Ver el contador en el navbar actualizarse

5. GESTIONAR EL CARRITO
   - Ir a: http://localhost:5000/saskia
   - Ver todos los productos añadidos
   - Modificar cantidades usando los inputs numéricos
   - Eliminar productos con el botón "Kendu / Eliminar"
   - Ver el total actualizado dinámicamente

6. CREAR PEDIDO
   - En la página del carrito, hacer clic en "Erosi / Comprar"
   - Confirmar la compra
   - El pedido se crea con precios históricos
   - El carrito se vacía automáticamente

7. VER PEDIDOS
   - Ir a: http://localhost:5000/api/eskaerak/view
   - Ver historial de pedidos con:
     * Número de pedido
     * Fecha
     * Estado (Ordainduta, Prestatzen, Bidean, Entregatuta)
     * Total
     * Lista de productos con precios históricos
   - Hacer clic en "Xehetasunak / Detalles" para ver más información

ENDPOINTS DE API REST:
======================

CARRITO (Saskia):
-----------------
POST   /api/saskia/gehitu      - Añadir producto al carrito
GET    /api/saskia/ikusi       - Ver contenido del carrito
PUT    /api/saskia/eguneratu   - Actualizar cantidad
DELETE /api/saskia/kendu       - Eliminar producto
DELETE /api/saskia/hustu       - Vaciar carrito completo

PEDIDOS (Eskaerak):
-------------------
POST   /api/eskaerak/sortu           - Crear pedido desde carrito
GET    /api/eskaerak/zerrenda        - Listar todos los pedidos
GET    /api/eskaerak/<id>            - Ver detalle de un pedido
PUT    /api/eskaerak/egoera/<id>    - Actualizar estado del pedido

PRODUCTOS:
----------
GET    /produktuak                   - Ver catálogo
GET    /produktuak?kategoria_id=X   - Filtrar por categoría
GET    /produktuak/api/list         - API JSON de productos

EJEMPLOS DE USO DE API:
=======================

1. Añadir producto al carrito:
curl -X POST http://localhost:5000/api/saskia/gehitu \
  -H "Content-Type: application/json" \
  -d '{"produktu_id": 1, "kantitatea": 2}'

2. Ver carrito:
curl http://localhost:5000/api/saskia/ikusi

3. Crear pedido:
curl -X POST http://localhost:5000/api/eskaerak/sortu

4. Ver pedidos:
curl http://localhost:5000/api/eskaerak/zerrenda

CARACTERÍSTICAS IMPORTANTES:
============================

CARRITO (SASKIA) - TEMPORAL:
- Es editable en cualquier momento
- Los precios se calculan dinámicamente del catálogo actual
- Si cambia el precio de un producto, el carrito muestra el nuevo precio
- Se puede modificar cantidades y eliminar productos
- Un carrito activo por usuario

PEDIDOS (ESKAERAK) - PERMANENTE:
- NO son editables una vez creados
- Guardan el precio histórico del momento de la compra
- Aunque cambien los precios en el catálogo, el pedido mantiene sus precios
- Solo se puede cambiar el estado (Ordainduta → Prestatzen → Bidean → Entregatuta)
- Representan transacciones comerciales reales

DATOS DE PRUEBA:
================

La base de datos viene precargada con:
- 4 categorías de productos
- 12 productos de ejemplo con precios

Puedes crear tu propio usuario o usar estos datos:

Categorías disponibles:
1. Ordenagailuak / Ordenadores
2. Telefonoak / Teléfonos
3. Tabletoak / Tablets
4. Osagarriak / Accesorios

Productos de ejemplo:
- MacBook Pro 14" (2499.99 €)
- iPhone 15 Pro (1199.99 €)
- iPad Air (699.99 €)
- AirPods Pro 2 (279.99 €)
... y más

ARQUITECTURA:
============

Backend: Flask (Python) con arquitectura MVC
Base de datos: SQLite con SQLAlchemy ORM
Frontend: HTML + CSS + JavaScript vanilla
API: REST con formato JSON
Autenticación: Sesiones de Flask con contraseñas hasheadas

ARCHIVOS IMPORTANTES:
====================

app.py              - Aplicación principal Flask
config.py           - Configuración
init_db.py          - Script de inicialización
models/             - Modelos de base de datos (SQLAlchemy)
routes/             - Controladores (Flask Blueprints)
templates/          - Vistas HTML (Jinja2)
static/             - CSS y JavaScript
technowave.db       - Base de datos SQLite

PARA REINICIAR LA BASE DE DATOS:
=================================

python init_db.py

Esto eliminará todos los datos existentes y recreará la BD con datos de ejemplo.

DETENER LA APLICACIÓN:
======================

Presionar CTRL+C en la terminal donde está corriendo Flask

SOPORTE:
========

Este proyecto implementa todas las especificaciones requeridas:
✓ Autenticación de usuarios
✓ Catálogo de productos por categorías
✓ Carrito temporal y editable (saskia)
✓ Sistema de pedidos permanentes (eskaerak)
✓ Precios históricos en pedidos
✓ API REST
✓ Arquitectura MVC
✓ Nombres en euskera según especificaciones
"""

print(__doc__)
