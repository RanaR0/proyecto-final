/**
 * Manejo global del tema oscuro/claro
 * - Detecta preferencia del sistema
 * - Persiste en localStorage
 * - Aplica clases CSS dinámicas
 */

document.addEventListener('DOMContentLoaded', function() {
  const body = document.getElementById('body');

  if (!body) return;

  // Detectar preferencia del sistema
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('theme');

  // Aplicar tema guardado o preferencia del sistema
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    body.classList.add('dark');
  }

  // Función para toggle del tema
  window.toggleTheme = function () {
    body.classList.toggle('dark');
    const isDark = body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Actualizar estado del toggle si existe
    const toggle = document.getElementById('theme-toggle');
    if (toggle) toggle.checked = isDark;
  };

  // Establecer estado inicial del toggle
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.checked = body.classList.contains('dark');
  }
});
