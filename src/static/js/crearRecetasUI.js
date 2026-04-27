/**
 * Manejo de UI para crear recetas
 * - Foto principal (trigger, preview)
 */

document.addEventListener('DOMContentLoaded', function() {
  // Manejo de foto principal
  const fotoPrincipalTrigger = document.getElementById("foto_principal_trigger");
  const fotoPrincipalInput = document.getElementById("foto_principal");

  if (fotoPrincipalTrigger && fotoPrincipalInput) {
    fotoPrincipalTrigger.addEventListener("click", () => {
      fotoPrincipalInput.click();
    });

    fotoPrincipalInput.addEventListener("change", (e) => {
      // Vista previa de la imagen
      if (e.target.files.length > 0) {
        fotoPrincipalTrigger.innerHTML = `
          <img src="${URL.createObjectURL(e.target.files[0])}"
              class="w-full h-full object-cover rounded-xl" />
        `;
      }
    });
  }
});
