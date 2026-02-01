#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║              TECHNOWAVE - INICIO RÁPIDO                  ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verificar si existe la base de datos
if [ ! -f "technowave.db" ]; then
    echo "⚠️  Base de datos no encontrada. Inicializando..."
    python init_db.py
    echo ""
fi

echo "🚀 Iniciando TechnoWave..."
echo ""
echo "📍 La aplicación estará disponible en:"
echo "   http://localhost:5000"
echo ""
echo "📝 Endpoints principales:"
echo "   - Página principal:     http://localhost:5000"
echo "   - Registro:            http://localhost:5000/auth/register"
echo "   - Login:               http://localhost:5000/auth/login"
echo "   - Catálogo:            http://localhost:5000/produktuak"
echo "   - Carrito:             http://localhost:5000/saskia"
echo "   - Pedidos:             http://localhost:5000/api/eskaerak/view"
echo ""
echo "⌨️  Presiona CTRL+C para detener el servidor"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Iniciar la aplicación
python app.py
