/**
 * Funciones para la página de perfil
 * - Manejo de tabs
 */

function mostrarTab(tab) {
  // Ocultar todos los tabs
  const tabPub = document.getElementById('tab-publicadas-content');
  const tabLikes = document.getElementById('tab-likes-content');
  const tabSeguidos = document.getElementById('tab-seguidos-content');

  if (tabPub) tabPub.classList.add('hidden');
  if (tabLikes) tabLikes.classList.add('hidden');
  if (tabSeguidos) tabSeguidos.classList.add('hidden');

  // Remover estilos activos de botones
  const btnPub = document.getElementById('tab-publicadas');
  const btnLikes = document.getElementById('tab-likes');
  const btnSeguidos = document.getElementById('tab-seguidos');

  if (btnPub) {
    btnPub.style.color = 'var(--text-secondary)';
    btnPub.style.borderBottom = '2px solid transparent';
  }
  if (btnLikes) {
    btnLikes.style.color = 'var(--text-secondary)';
    btnLikes.style.borderBottom = '2px solid transparent';
  }
  if (btnSeguidos) {
    btnSeguidos.style.color = 'var(--text-secondary)';
    btnSeguidos.style.borderBottom = '2px solid transparent';
  }

  // Mostrar el tab seleccionado
  const selectedContent = document.getElementById('tab-' + tab + '-content');
  const selectedBtn = document.getElementById('tab-' + tab);

  if (selectedContent) selectedContent.classList.remove('hidden');
  if (selectedBtn) {
    selectedBtn.style.color = '#d97706';
    selectedBtn.style.borderBottom = '2px solid #d97706';
  }
}
