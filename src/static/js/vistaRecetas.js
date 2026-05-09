/**
 * Añade funcionalidad de marcado visual a los ingredientes.
 * 
 * Cuando un checkbox cambia de estado, se aplica o elimina un estilo
 * visual (tachado y cambio de color) al texto del ingrediente asociado.
 */

document.querySelectorAll('.ingredient-check').forEach((checkbox) => {

    // Escucha cambios en cada checkbox de ingrediente
    checkbox.addEventListener('change', function () {

        // Elemento de texto asociado al checkbox (siguiente elemento en el DOM)
        const text = this.nextElementSibling;

        // Si el ingrediente está marcado como completado
        if (this.checked) {
            text.classList.add('line-through', 'text-stone-400');
        } 
        // Si se desmarca, se restauran los estilos originales
        else {
            text.classList.remove('line-through', 'text-stone-400');
        }
    });
});