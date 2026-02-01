// Gestión del carrito (saskia)
// IMPORTANTE: El carrito es TEMPORAL y EDITABLE
// Los precios se calculan dinámicamente del catálogo actual

document.addEventListener('DOMContentLoaded', function() {
    // Actualizar contador del carrito en el navbar
    actualizarKontadorea();
});

// Actualizar contador del carrito
async function actualizarKontadorea() {
    try {
        const response = await fetch('/api/saskia/ikusi');
        const data = await response.json();
        
        if (data.success) {
            const totalItems = data.items.reduce((sum, item) => sum + item.kantitatea, 0);
            const badge = document.getElementById('saski-kantitatea');
            if (badge) {
                badge.textContent = totalItems;
                badge.style.display = totalItems > 0 ? 'inline-block' : 'none';
            }
        }
    } catch (error) {
        console.error('Error actualizando contador:', error);
    }
}

// Añadir producto al carrito
async function gehituSaskira(produktuId, produktuIzena) {
    try {
        const data = await fetchAPI('/api/saskia/gehitu', {
            method: 'POST',
            body: JSON.stringify({
                produktu_id: produktuId,
                kantitatea: 1
            })
        });
        
        if (data.success) {
            showNotification(`${produktuIzena} saskira gehitu da / añadido al carrito`, 'success');
            actualizarKontadorea();
        }
    } catch (error) {
        showNotification('Errorea saskira gehitzean / Error al añadir al carrito', 'danger');
    }
}

// Cargar el carrito completo (para la página de saskia)
async function kargatuSaskia() {
    const edukia = document.getElementById('saskia-edukia');
    const totala = document.getElementById('saskia-totala');
    const hutsik = document.getElementById('saskia-hutsik');
    
    try {
        const response = await fetch('/api/saskia/ikusi');
        const data = await response.json();
        
        if (data.success && data.items.length > 0) {
            // Carrito con productos
            edukia.innerHTML = renderSaskiItems(data.items);
            document.getElementById('total-prezioa').textContent = data.totala.toFixed(2);
            totala.style.display = 'block';
            hutsik.style.display = 'none';
            
            // Añadir event listeners
            addSaskiEventListeners();
        } else {
            // Carrito vacío
            edukia.innerHTML = '';
            totala.style.display = 'none';
            hutsik.style.display = 'block';
        }
    } catch (error) {
        edukia.innerHTML = '<p class="error">Errorea saskia kargatzean / Error al cargar el carrito</p>';
    }
}

// Renderizar items del carrito
function renderSaskiItems(items) {
    return `
        <div class="saskia-taula">
            <table>
                <thead>
                    <tr>
                        <th>Produktua / Producto</th>
                        <th>Prezioa / Precio</th>
                        <th>Kantitatea / Cantidad</th>
                        <th>Subtotala / Subtotal</th>
                        <th>Akzioak / Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    ${items.map(item => `
                        <tr data-produktu-id="${item.produktu_id}">
                            <td>
                                ${item.irudi_urla ? `<img src="${item.irudi_urla}" alt="${item.produktu_izena}" class="mini-irudia">` : ''}
                                ${item.produktu_izena}
                            </td>
                            <td>${item.prezioa.toFixed(2)} €</td>
                            <td>
                                <input type="number" 
                                       class="kantitatea-input" 
                                       value="${item.kantitatea}" 
                                       min="1" 
                                       data-produktu-id="${item.produktu_id}">
                            </td>
                            <td class="subtotal">${item.subtotala.toFixed(2)} €</td>
                            <td>
                                <button class="btn btn-sm btn-danger btn-kendu" 
                                        data-produktu-id="${item.produktu_id}">
                                    Kendu / Eliminar
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// Añadir event listeners a los elementos del carrito
function addSaskiEventListeners() {
    // Actualizar cantidad
    document.querySelectorAll('.kantitatea-input').forEach(input => {
        input.addEventListener('change', async function() {
            const produktuId = this.dataset.produktuId;
            const kantitatea = parseInt(this.value);
            
            if (kantitatea < 1) {
                this.value = 1;
                return;
            }
            
            await eguneratuKantitatea(produktuId, kantitatea);
        });
    });
    
    // Eliminar producto
    document.querySelectorAll('.btn-kendu').forEach(button => {
        button.addEventListener('click', async function() {
            const produktuId = this.dataset.produktuId;
            await kenduSaskitik(produktuId);
        });
    });
    
    // Botón comprar
    const btnErosi = document.getElementById('btn-erosi');
    if (btnErosi) {
        btnErosi.addEventListener('click', sortuEskaera);
    }
    
    // Botón vaciar carrito
    const btnHustu = document.getElementById('btn-hustu');
    if (btnHustu) {
        btnHustu.addEventListener('click', async function() {
            if (confirm('Ziur zaude saskia hustea nahi duzula? / ¿Seguro que quieres vaciar el carrito?')) {
                await hustuSaskia();
            }
        });
    }
}

// Actualizar cantidad de un producto
async function eguneratuKantitatea(produktuId, kantitatea) {
    try {
        const data = await fetchAPI('/api/saskia/eguneratu', {
            method: 'PUT',
            body: JSON.stringify({
                produktu_id: produktuId,
                kantitatea: kantitatea
            })
        });
        
        if (data.success) {
            kargatuSaskia(); // Recargar carrito
            actualizarKontadorea();
        }
    } catch (error) {
        showNotification('Errorea kantitatea eguneratzean / Error al actualizar cantidad', 'danger');
    }
}

// Eliminar producto del carrito
async function kenduSaskitik(produktuId) {
    try {
        const data = await fetchAPI('/api/saskia/kendu', {
            method: 'DELETE',
            body: JSON.stringify({
                produktu_id: produktuId
            })
        });
        
        if (data.success) {
            showNotification(data.message, 'success');
            kargatuSaskia();
            actualizarKontadorea();
        }
    } catch (error) {
        showNotification('Errorea produktua kentzean / Error al eliminar producto', 'danger');
    }
}

// Vaciar carrito completo
async function hustuSaskia() {
    try {
        const data = await fetchAPI('/api/saskia/hustu', {
            method: 'DELETE'
        });
        
        if (data.success) {
            showNotification(data.message, 'success');
            kargatuSaskia();
            actualizarKontadorea();
        }
    } catch (error) {
        showNotification('Errorea saskia hustean / Error al vaciar carrito', 'danger');
    }
}

// Crear pedido desde el carrito
async function sortuEskaera() {
    if (!confirm('Erosketa baieztatu nahi duzu? / ¿Confirmar compra?')) {
        return;
    }
    
    try {
        const data = await fetchAPI('/api/eskaerak/sortu', {
            method: 'POST'
        });
        
        if (data.success) {
            showNotification('Eskaera arrakastaz sortuta! / ¡Pedido creado con éxito!', 'success');
            setTimeout(() => {
                window.location.href = '/api/eskaerak/view';
            }, 1500);
        }
    } catch (error) {
        showNotification(error.message || 'Errorea eskaera sortzean / Error al crear pedido', 'danger');
    }
}

// Si estamos en la página de saskia, cargar automáticamente
if (window.location.pathname.includes('/saskia')) {
    document.addEventListener('DOMContentLoaded', kargatuSaskia);
}
