/**
 * Interfaz de usuario para la edición de recetas
 * 
 * Funcionalidades:
 * - Cambio de versión de la receta
 * - Selección y vista previa de imagen principal
 */

document.addEventListener('DOMContentLoaded', function () {

  /**
   * ============================
   * MANEJO DE VERSIONES
   * ============================
   */

  const versionSelector = document.getElementById('version-selector');

  if (versionSelector) {

    versionSelector.addEventListener('change', function () {

      // ID de la receta actual en edición
      const recetaId = document.querySelector('input[name="receta_id"]')?.value;

      // Si el usuario selecciona una versión distinta
      if (this.value !== recetaId) {

        // Confirmación para evitar pérdida de cambios
        if (confirm('¿Estás seguro? Esto eliminará todas las versiones más nuevas.')) {
          window.location.href = `/crear/cargar_version/${this.value}`;
        }
      }
    });
  }


  /**
   * ============================
   * MANEJO DE IMAGEN PRINCIPAL
   * ============================
   */

  const fotoPrincipalTrigger = document.getElementById("foto_principal_trigger");
  const fotoPrincipalInput = document.getElementById("foto_principal");

  if (fotoPrincipalTrigger && fotoPrincipalInput) {

    /**
     * Abre el selector de archivos al hacer clic en el contenedor
     */
    fotoPrincipalTrigger.addEventListener("click", () => {
      fotoPrincipalInput.click();
    });

    /**
     * Muestra una vista previa de la imagen seleccionada
     */
    fotoPrincipalInput.addEventListener("change", (e) => {

      if (e.target.files.length > 0) {

        const file = e.target.files[0];

        fotoPrincipalTrigger.innerHTML = `
          <img src="${URL.createObjectURL(file)}"
              class="w-full h-full object-cover rounded-xl" />
        `;
      }
    });
  }
});