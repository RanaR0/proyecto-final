/**
 * Sistema de búsqueda y carga infinita de recetas
 * 
 * Funcionalidades:
 * - Búsqueda con debounce (tiempo de espera)
 * - Carga paginada de resultados (infinite scroll)
 * - Renderizado dinámico de tarjetas de recetas
 * - Manejo de estados: loading, error, sin resultados
 */

document.addEventListener('DOMContentLoaded', function () {

  // Elementos del DOM necesarios para la búsqueda
  const searchInput = document.getElementById('search-input');
  const recetasGrid = document.getElementById('recetas-grid');
  const loader = document.getElementById('loader');

  // Si falta algún elemento, no se ejecuta la funcionalidad
  if (!searchInput || !recetasGrid || !loader) return;

  // Estado de la paginación y control de carga
  let currentPage = 1;
  let isLoading = false;
  let hasMore = true;
  let searchTimeout;

  /**
   * Carga recetas desde la API
   * Puede usarse para búsqueda o scroll infinito
   */
  async function loadMoreRecipes(isSearch = false) {

    // Evita múltiples peticiones simultáneas
    if (isLoading || !hasMore) return;

    isLoading = true;

    /**
     * Muestra loader cuando:
     * - No es la primera página
     * - O es una búsqueda nueva
     */
    if (currentPage > 1 || isSearch) {
      loader.classList.remove('hidden');

      loader.innerHTML = isSearch
        ? '<p class="text-stone-600">Buscando recetas...</p>'
        : '<p class="text-stone-600">Cargando recetas...</p>';
    }

    try {

      // Texto actual de búsqueda
      const searchTerm = searchInput.value.trim();

      // Construcción de URL con paginación y query opcional
      const url = `/api/busqueda?page=${currentPage}&limit=20${
        searchTerm ? `&q=${encodeURIComponent(searchTerm)}` : ''
      }`;

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error('Error en la petición');
      }

      const data = await response.json();

      /**
       * Caso: no hay resultados en la primera página
       */
      if (currentPage === 1 && (!data.recetas || data.recetas.length === 0)) {

        recetasGrid.innerHTML = `
          <div class="col-span-full text-center py-12">
            <i class="fas fa-search text-4xl text-stone-400 mb-4"></i>
            <p class="text-stone-600">No se encontraron recetas</p>
          </div>
        `;

        hasMore = false;
        loader.classList.add('hidden');
        return;
      }

      /**
       * Renderizado de recetas obtenidas
       */
      if (data.recetas && data.recetas.length > 0) {

        data.recetas.forEach(r => {

          const card = document.createElement('div');

          // Estilos de la tarjeta
          card.className =
            'receta-card relative group cursor-pointer overflow-hidden rounded-lg bg-stone-200 aspect-square';

          // Redirección al detalle de receta
          card.onclick = () => {
            window.location.href = `/receta/${r.id}`;
          };

          let imgHtml = '';

          /**
           * Imagen de la receta o placeholder si no existe
           */
          if (r.foto) {
            imgHtml = `
              <img
                src="/static/${r.foto}"
                alt="${r.titulo}"
                class="w-full h-full object-cover group-hover:scale-105 transition duration-300"
              >
            `;
          } else {
            imgHtml = `
              <div class="w-full h-full bg-stone-300 flex items-center justify-center text-stone-500">
                <i class="fas fa-utensils text-2xl"></i>
              </div>
            `;
          }

          // Estructura final de la tarjeta
          card.innerHTML = `
            ${imgHtml}

            <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition duration-300 flex flex-col justify-end p-3">

              <div class="text-white opacity-0 group-hover:opacity-100 transition duration-300">

                <h3 class="font-semibold text-sm truncate">
                  ${r.titulo}
                </h3>

                <div class="flex items-center gap-1 text-xs">
                  <i class="fas fa-heart text-red-500"></i>
                  <span>${r.likes}</span>
                </div>

              </div>
            </div>
          `;

          recetasGrid.appendChild(card);
        });

        // Avanza la paginación
        currentPage++;

        loader.classList.add('hidden');
      } else {

        /**
         * Caso: no hay más recetas
         */
        hasMore = false;

        loader.classList.remove('hidden');
        loader.innerHTML =
          '<p class="text-stone-500">No hay más recetas</p>';
      }

    } catch (error) {

      console.error('Error loading recipes:', error);

      loader.classList.remove('hidden');
      loader.innerHTML =
        '<p class="text-red-500">Error al cargar recetas</p>';

    } finally {
      isLoading = false;
    }
  }

  /**
   * Reinicia búsqueda y carga resultados desde cero
   */
  function performSearch() {
    currentPage = 1;
    hasMore = true;
    recetasGrid.innerHTML = '';
    loadMoreRecipes(true);
  }

  /**
   * Búsqueda con debounce para evitar muchas peticiones
   */
  searchInput.addEventListener('input', () => {

    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {
      performSearch();
    }, 300);
  });

  /**
   * Infinite scroll: carga más recetas al llegar al final
   */
  window.addEventListener('scroll', () => {

    if (
      window.innerHeight + window.scrollY >=
      document.body.offsetHeight - 500
    ) {
      loadMoreRecipes(false);
    }
  });

  // Carga inicial
  loadMoreRecipes(false);
});