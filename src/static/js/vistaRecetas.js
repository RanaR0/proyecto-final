// Script para tachar los ingredienetes
document.querySelectorAll('.ingredient-check').forEach((checkbox) => {
    checkbox.addEventListener('change', function () {
        const text = this.nextElementSibling;
        if (this.checked) {
        text.classList.add('line-through', 'text-stone-400');
        } else {
        text.classList.remove('line-through', 'text-stone-400');
        }
    });
});