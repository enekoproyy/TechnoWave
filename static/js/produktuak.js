// Gestión de productos

document.addEventListener('DOMContentLoaded', function() {
    // Añadir event listeners a los botones de añadir al carrito
    const botonesGehitu = document.querySelectorAll('.btn-gehitu-saskira');
    
    botonesGehitu.forEach(button => {
        button.addEventListener('click', function() {
            const produktuId = parseInt(this.dataset.produktuId);
            const produktuIzena = this.dataset.produktuIzena;
            
            gehituSaskira(produktuId, produktuIzena);
        });
    });
});
