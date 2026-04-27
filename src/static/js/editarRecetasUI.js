/**
 * Manejo de UI para editar recetas
 * - Selector de versiones
 * - Foto principal (trigger, preview)
 */

document.addEventListener('DOMContentLoaded', function() {
  // Manejo de versiones
  const versionSelector = document.getElementById('version-selector');
  if (versionSelector) {
    versionSelector.addEventListener('change', function () {
      const recetaId = document.querySelector('input[name="receta_id"]')?.value;
      if (this.value !== recetaId) {
        if (confirm('¿Estás seguro? Esto eliminará todas las versiones más nuevas.')) {
          window.location.href = `/crear/cargar_version/${this.value}`;
        }
      }
    });
  }

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
