# TechnoWave - Tienda Online

Aplicación web de tienda online desarrollada con Flask, SQLite y SQLAlchemy.

## 🚀 Características

- ✅ **Autenticación de usuarios** (registro, login, logout)
- ✅ **Catálogo de productos** organizado por categorías
- ✅ **Carrito de compra (saskia)** temporal y editable
- ✅ **Sistema de pedidos (eskaerak)** permanentes con precios históricos
- ✅ **API REST** para carrito y pedidos
- ✅ **Arquitectura MVC** con Flask Blueprints
- ✅ **Interfaz responsive** con HTML + CSS + JavaScript

## 📋 Requisitos

- Python 3.8+
- Flask
- SQLAlchemy
- SQLite

## 🔧 Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Inicializar la base de datos con datos de ejemplo:
```bash
python init_db.py
```

3. Ejecutar la aplicación:
```bash
python app.py
```

4. Abrir en el navegador:
```
http://localhost:5000
```

## 🗄️ Estructura de la Base de Datos

### Usuarios (erabiltzaileak)
- `erabiltzaile_id` (PK)
- `helbide_elektronikoa` (email único)
- `pasahitza` (hash seguro)
- `izena`, `abizenak`, `tfnoa`, `sormen_data`

### Productos (produktuak)
- `produktu_id` (PK)
- `izena`, `deskribapena`, `prezioa`, `irudi_urla`
- `kategoria_id` (FK)

### Carrito (saski_elementuak) - TEMPORAL
- `erabiltzaile_id` (FK, PK)
- `produktu_id` (FK, PK)
- `kantitatea`

**Características:** Temporal, editable, precios dinámicos del catálogo

### Pedidos (eskaerak) - PERMANENTE
- `eskaera_id` (PK)
- `erabiltzaile_id` (FK)
- `sormen_data`, `egoera`

### Detalle pedidos (eskaera_elementuak)
- `eskaera_id` (FK, PK)
- `produktu_id` (FK, PK)
- `kantitatea`, `prezioa` (histórico)

**Características:** Permanentes, no editables, guardan precios históricos

## 🔄 Lógica de Negocio

### Carrito → Pedido
1. Usuario añade productos al carrito
2. Puede modificar cantidades o eliminar
3. Al confirmar compra: se crea pedido, se guardan precios históricos, se vacía carrito

### Estados del Pedido
**Ordainduta** → **Prestatzen** → **Bidean** → **Entregatuta**

## 🛠️ Estructura del Proyecto

```
TechnoWave/
├── app.py                  # Aplicación principal
├── config.py              # Configuración
├── init_db.py             # Script inicialización
├── models/                # Modelos SQLAlchemy
├── routes/                # Rutas Flask
├── templates/             # HTML
├── static/                # CSS + JS
└── utils/                 # Utilidades
```

## 🔐 API Endpoints

**Autenticación:** `/auth/register`, `/auth/login`, `/auth/logout`

**Productos:** `/produktuak`, `/produktuak/<id>`

**Carrito:** `/api/saskia/gehitu`, `/api/saskia/ikusi`, `/api/saskia/eguneratu`, `/api/saskia/kendu`

**Pedidos:** `/api/eskaerak/sortu`, `/api/eskaerak/zerrenda`, `/api/eskaerak/<id>`

## 📝 Notas Importantes

- **El carrito es temporal**: Precios dinámicos del catálogo
- **Los pedidos son permanentes**: Guardan precios históricos
- **Nomenclatura en euskera**: Respeta nombres requeridos en BD

## 📄 Licencia

MIT License - TechnoWave 2026