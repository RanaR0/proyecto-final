/**
 * Búsqueda de recetas con infinite scroll y búsqueda en tiempo real
 */

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('search-input');
  const recetasGrid = document.getElementById('recetas-grid');
  const loader = document.getElementById('loader');

  if (!searchInput || !recetasGrid || !loader) return;

  let currentPage = 1;
  let isLoading = false;
  let hasMore = true;
  let searchTimeout;

  // Cargar recetas
  async function loadMoreRecipes() {
    if (isLoading || !hasMore) return;

    isLoading = true;
    loader.classList.remove('hidden');
    loader.innerHTML = '<i class="fas fa-spinner fa-spin text-stone-500"></i>';

    try {
      const searchTerm = searchInput.value.trim();

      // AQUÍ estaba uno de los errores:
      // NO debe ser currentPage + 1
      const url = `/api/busqueda?page=${currentPage}&limit=20${
        searchTerm ? `&q=${encodeURIComponent(searchTerm)}` : ''
      }`;

      const response = await fetch(url);
      const data = await response.json();

      if (data.recetas && data.recetas.length > 0) {
        data.recetas.forEach(r => {
          const card = document.createElement('div');

          card.className =
            'receta-card relative group cursor-pointer overflow-hidden rounded-lg bg-stone-200 aspect-square';

          card.onclick = () => {
            window.location.href =
              `/receta/${r.id}`;
          };

          let imgHtml = '';

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

        // Incrementamos SOLO después de cargar bien
        currentPage++;
      } else {
        hasMore = false;

        if (currentPage === 1) {
          loader.innerHTML =
            '<p class="text-stone-500">No se encontraron recetas</p>';
        } else {
          loader.innerHTML =
            '<p class="text-stone-500">No hay más recetas</p>';
        }
      }
    } catch (error) {
      console.error('Error loading recipes:', error);
      loader.innerHTML =
        '<p class="text-red-500">Error al cargar recetas</p>';
    } finally {
      isLoading = false;
    }
  }

  // Nueva búsqueda
  function performSearch() {
    currentPage = 1;
    hasMore = true;

    recetasGrid.innerHTML = '';
    loader.innerHTML = '';

    loadMoreRecipes();
  }

  // Búsqueda en tiempo real con debounce
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {
      performSearch();
    }, 300);
  });

  // Infinite scroll
  window.addEventListener('scroll', () => {
    if (
      window.innerHeight + window.scrollY >=
      document.body.offsetHeight - 500
    ) {
      loadMoreRecipes();
    }
  });

  // Primera carga inicial
  loadMoreRecipes();
});