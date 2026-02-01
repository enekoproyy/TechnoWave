// Funciones generales de la aplicación

// Cerrar alertas
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    // Auto-cerrar alertas después de 5 segundos
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const container = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button class="close-alert">&times;</button>
    `;
    
    container.insertBefore(alert, container.firstChild);
    
    // Añadir evento de cierre
    alert.querySelector('.close-alert').addEventListener('click', function() {
        alert.style.display = 'none';
    });
    
    // Auto-cerrar
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// Función para hacer peticiones fetch con manejo de errores
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Errorea / Error');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
