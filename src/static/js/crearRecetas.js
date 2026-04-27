document.getElementById("add-ingrediente").addEventListener("click", () => {
    const cont = document.getElementById("ingredientes-container");

    const div = document.createElement("div");
    div.className = "flex gap-3 ingrediente-item";

    div.innerHTML = `
        <input type="text" name="ingredientes[]" placeholder="Ej: 200g de pasta"
            class="flex-1 rounded-lg border border-stone-300 px-3 py-2 text-sm" />
        <button type="button" class="remove-ingrediente text-red-600 font-bold">✕</button>
    `;

    cont.appendChild(div);
});

document.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-ingrediente")) {
        e.target.parentElement.remove();
    }
});


// ---------------------- PASOS ---------------------- //

document.getElementById("add-paso").addEventListener("click", () => {
    const cont = document.getElementById("pasos-container");
    const num = cont.children.length + 1;

    // Detectar si estamos en modo tema oscuro (editar) o modo claro (crear)
    const root = document.documentElement;
    const bgSecondary = getComputedStyle(root).getPropertyValue('--bg-secondary').trim();
    const isThemedMode = bgSecondary && bgSecondary !== '';

    const div = document.createElement("div");

    if (isThemedMode) {
        // Modo editar (con variables CSS)
        div.className = "paso-item p-4 rounded-lg space-y-3";
        div.style.backgroundColor = "var(--bg-secondary)";
        div.style.border = "1px solid var(--border)";

        div.innerHTML = `
            <div class="flex items-start justify-between gap-3">
                <div class="flex items-start gap-3 flex-1">
                    <div class="numero-paso w-8 h-8 flex items-center justify-center rounded-full text-white text-sm font-semibold flex-shrink-0 mt-0.5"
                        style="background-color: #d97706;">
                        ${num}
                    </div>
                    <textarea name="pasos[]" rows="2" placeholder="Describe este paso..."
                        class="flex-1 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-800 resize-none"
                        style="background-color: var(--input-bg); color: var(--input-text); border: 1px solid var(--input-border);"></textarea>
                </div>
                <button type="button" class="remove-paso text-red-600 font-bold text-lg hover:text-red-700 flex-shrink-0">✕</button>
            </div>
        `;
    } else {
        // Modo crear (con clases Tailwind stone)
        div.className = "paso-item p-4 rounded-lg bg-stone-50 border border-stone-200 space-y-3";

        div.innerHTML = `
            <div class="flex items-start justify-between gap-3">
                <div class="flex items-start gap-3 flex-1">
                    <div class="numero-paso w-8 h-8 flex items-center justify-center rounded-full bg-amber-800 text-white text-xs font-semibold flex-shrink-0 mt-0.5">
                        ${num}
                    </div>
                    <textarea name="pasos[]" rows="2" placeholder="Describe este paso..."
                        class="flex-1 rounded-lg border border-stone-300 px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-amber-800"></textarea>
                </div>
                <button type="button" class="remove-paso text-red-600 font-bold text-lg hover:text-red-700 flex-shrink-0">✕</button>
            </div>
        `;
    }

    cont.appendChild(div);
});

document.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-paso")) {
        e.target.closest(".paso-item").remove();

        // Reenumerar pasos
        const pasos = document.querySelectorAll(".paso-item .numero-paso");
        pasos.forEach((p, i) => p.textContent = i + 1);
    }
});

// Event de foto para pasos
document.addEventListener("change", (e) => {
    if (e.target.name === "fotos_pasos[]") {
        const label = e.target.closest("label");
        if (e.target.files.length > 0) {
            label.innerHTML = `
                <img src="${URL.createObjectURL(e.target.files[0])}"
                    class="w-full h-full object-cover rounded-lg" />
            `;
        }
    }
});
