/**
 * Sistema de modal para errores de validación en formularios
 * 
 * - Crea el modal dinámicamente si no existe en el DOM
 * - Muestra mensajes de error de forma visual al usuario
 * - Permite cerrar el modal con botón o clic fuera
 */

function showErrorModal(errorMessage) {

  /**
   * Si el modal no existe aún, se crea dinámicamente
   * para evitar duplicaciones en el DOM
   */
  if (!document.getElementById("error-modal")) {

    const modal = document.createElement("div");
    modal.id = "error-modal";

    // Estructura HTML del modal
    modal.innerHTML = `
      <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-xl max-w-sm w-full mx-4 p-6">
          <div class="flex items-start gap-4">

            <!-- Icono de error -->
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <!-- Contenido del modal -->
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Error de Validación</h3>

              <!-- Mensaje dinámico del error -->
              <p class="text-sm text-gray-600 mb-4" id="error-message"></p>

              <!-- Botón para cerrar el modal -->
              <button id="error-close"
                class="w-full px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition">
                Entendido
              </button>
            </div>

          </div>
        </div>
      </div>
    `;

    // Añade el modal al body
    document.body.appendChild(modal);

    /**
     * Evento: cerrar modal al pulsar el botón
     */
    document.getElementById("error-close").addEventListener("click", function () {
      modal.style.display = "none";
    });

    /**
     * Evento: cerrar modal al hacer clic fuera del contenido
     */
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        modal.style.display = "none";
      }
    });
  }

  /**
   * Muestra el modal con el mensaje de error recibido
   */
  const modal = document.getElementById("error-modal");
  document.getElementById("error-message").textContent = errorMessage;
  modal.style.display = "flex";
}


/**
 * Si existe un error generado desde el backend,
 * se muestra automáticamente al cargar la página
 */
document.addEventListener("DOMContentLoaded", function () {

  const errorDiv = document.getElementById("error-modal-trigger");

  if (errorDiv) {
    const errorMessage = errorDiv.getAttribute("data-error");

    if (errorMessage) {
      showErrorModal(errorMessage);
    }
  }
});