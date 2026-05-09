/**
 * Manejo de selección y vista previa de la imagen principal
 * en el formulario de recetas.
 * 
 * - Abre el selector de archivos al hacer clic en el contenedor
 * - Muestra una vista previa de la imagen seleccionada
 */

document.addEventListener('DOMContentLoaded', function () {

  // Elemento visual que actúa como botón para seleccionar imagen
  const fotoPrincipalTrigger = document.getElementById("foto_principal_trigger");

  // Input real de tipo file oculto
  const fotoPrincipalInput = document.getElementById("foto_principal");

  /**
   * Si ambos elementos existen, se configuran los eventos
   */
  if (fotoPrincipalTrigger && fotoPrincipalInput) {

    /**
     * Al hacer clic en el contenedor, se abre el selector de archivos
     */
    fotoPrincipalTrigger.addEventListener("click", () => {
      fotoPrincipalInput.click();
    });

    /**
     * Cuando el usuario selecciona una imagen:
     * - Se genera una URL temporal
     * - Se muestra una vista previa en el contenedor
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