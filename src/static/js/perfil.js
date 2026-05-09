/**
 * Sistema de pestañas (tabs) en la página de perfil
 * 
 * Permite cambiar entre:
 * - Recetas publicadas
 * - Recetas con likes
 * - Usuarios seguidos
 * 
 * Gestiona:
 * - Visibilidad de secciones
 * - Estilos activos de los botones
 */

function mostrarTab(tab) {

  /**
   * Oculta todas las secciones de contenido del perfil
   */
  const tabPub = document.getElementById('tab-publicadas-content');
  const tabLikes = document.getElementById('tab-likes-content');
  const tabSeguidos = document.getElementById('tab-seguidos-content');

  if (tabPub) tabPub.classList.add('hidden');
  if (tabLikes) tabLikes.classList.add('hidden');
  if (tabSeguidos) tabSeguidos.classList.add('hidden');

  /**
   * Restablece el estilo de todos los botones de navegación
   * (estado inactivo)
   */
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

  /**
   * Muestra únicamente la sección seleccionada
   * y activa el estilo del botón correspondiente
   */
  const selectedContent = document.getElementById('tab-' + tab + '-content');
  const selectedBtn = document.getElementById('tab-' + tab);

  if (selectedContent) selectedContent.classList.remove('hidden');

  if (selectedBtn) {
    selectedBtn.style.color = '#d97706';
    selectedBtn.style.borderBottom = '2px solid #d97706';
  }
}