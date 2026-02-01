// Gestión de pedidos (eskaerak)
// IMPORTANTE: Los pedidos son PERMANENTES y NO EDITABLES
// Solo se puede cambiar el estado

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('/eskaerak')) {
        kargatuEskaerak();
    }
});

// Cargar lista de pedidos
async function kargatuEskaerak() {
    const zerrenda = document.getElementById('eskaerak-zerrenda');
    
    try {
        const response = await fetch('/api/eskaerak/zerrenda');
        const data = await response.json();
        
        if (data.success) {
            if (data.eskaerak.length > 0) {
                zerrenda.innerHTML = renderEskaerak(data.eskaerak);
                addEskaerakEventListeners();
            } else {
                zerrenda.innerHTML = `
                    <div class="empty-message">
                        <p>Oraindik ez duzu eskaera egin / Aún no has realizado ningún pedido</p>
                        <a href="/produktuak" class="btn btn-primary">Erosten hasi / Empezar a comprar</a>
                    </div>
                `;
            }
        }
    } catch (error) {
        zerrenda.innerHTML = '<p class="error">Errorea eskaerak kargatzean / Error al cargar pedidos</p>';
    }
}

// Renderizar pedidos
function renderEskaerak(eskaerak) {
    return eskaerak.map(eskaera => `
        <div class="eskaera-card">
            <div class="eskaera-header">
                <h3>Eskaera #${eskaera.eskaera_id}</h3>
                <span class="egoera egoera-${eskaera.egoera.toLowerCase()}">${eskaera.egoera}</span>
            </div>
            
            <div class="eskaera-info">
                <p><strong>Data / Fecha:</strong> ${new Date(eskaera.sormen_data).toLocaleString('eu-ES')}</p>
                <p><strong>Totala / Total:</strong> ${eskaera.totala.toFixed(2)} €</p>
            </div>
            
            <div class="eskaera-elementuak">
                <h4>Produktuak / Productos:</h4>
                <ul>
                    ${eskaera.elementuak.map(elem => `
                        <li>
                            ${elem.produktu_izena} - 
                            ${elem.kantitatea} unitate x ${elem.prezioa.toFixed(2)} € = 
                            ${elem.subtotala.toFixed(2)} €
                        </li>
                    `).join('')}
                </ul>
            </div>
            
            <div class="eskaera-akzioak">
                <button class="btn btn-sm btn-info btn-xehetasunak" 
                        data-eskaera-id="${eskaera.eskaera_id}">
                    Xehetasunak / Detalles
                </button>
            </div>
        </div>
    `).join('');
}

// Añadir event listeners
function addEskaerakEventListeners() {
    // Botón detalles
    document.querySelectorAll('.btn-xehetasunak').forEach(button => {
        button.addEventListener('click', function() {
            const eskaeraId = this.dataset.eskaeraId;
            ikusiXehetasunak(eskaeraId);
        });
    });
}

// Ver detalles de un pedido
async function ikusiXehetasunak(eskaeraId) {
    try {
        const response = await fetch(`/api/eskaerak/${eskaeraId}`);
        const data = await response.json();
        
        if (data.success) {
            mostrarModal(data.eskaera);
        }
    } catch (error) {
        showNotification('Errorea xehetasunak kargatzean / Error al cargar detalles', 'danger');
    }
}

// Mostrar modal con detalles del pedido
function mostrarModal(eskaera) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close">&times;</span>
            <h2>Eskaera #${eskaera.eskaera_id} - Xehetasunak / Detalles</h2>
            
            <div class="eskaera-detalle">
                <p><strong>Data / Fecha:</strong> ${new Date(eskaera.sormen_data).toLocaleString('eu-ES')}</p>
                <p><strong>Egoera / Estado:</strong> <span class="egoera egoera-${eskaera.egoera.toLowerCase()}">${eskaera.egoera}</span></p>
                
                <h3>Produktuak / Productos:</h3>
                <table class="detalle-taula">
                    <thead>
                        <tr>
                            <th>Produktua</th>
                            <th>Prezioa</th>
                            <th>Kantitatea</th>
                            <th>Subtotala</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${eskaera.elementuak.map(elem => `
                            <tr>
                                <td>${elem.produktu_izena}</td>
                                <td>${elem.prezioa.toFixed(2)} €</td>
                                <td>${elem.kantitatea}</td>
                                <td>${elem.subtotala.toFixed(2)} €</td>
                            </tr>
                        `).join('')}
                        <tr class="total-row">
                            <td colspan="3"><strong>TOTALA / TOTAL</strong></td>
                            <td><strong>${eskaera.totala.toFixed(2)} €</strong></td>
                        </tr>
                    </tbody>
                </table>
                
                <p class="info-nota">
                    ℹ️ Eskaera honek produktuen prezio historikoa gorde du / 
                    Este pedido guarda el precio histórico de los productos
                </p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Cerrar modal
    modal.querySelector('.modal-close').addEventListener('click', function() {
        modal.remove();
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
}
