/**
 * Manejo global del tema oscuro/claro
 * - Detecta preferencia del sistema
 * - Persiste en localStorage
 * - Aplica clases CSS dinámicas
 */

document.addEventListener('DOMContentLoaded', function() {
  const root = document.documentElement;
  const body = document.getElementById('body');

  if (!body) return;

  const applyTheme = (isDark) => {
    root.classList.toggle('dark', isDark);
    body.classList.toggle('dark', isDark);
  };

  // Detectar preferencia del sistema
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('theme');

  // Aplicar tema guardado o preferencia del sistema
  const shouldBeDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
  applyTheme(shouldBeDark);

  // Sincronizar por si el preloader ya aplicó el tema en <html>
  if (root.classList.contains('dark') && !body.classList.contains('dark')) {
    body.classList.add('dark');
  }

  // Función para toggle del tema
  window.toggleTheme = function () {
    const isDark = !root.classList.contains('dark');
    applyTheme(isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Actualizar estado del toggle si existe
    const toggle = document.getElementById('theme-toggle');
    if (toggle) toggle.checked = isDark;
  };

  // Establecer estado inicial del toggle
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.checked = root.classList.contains('dark');
  }

  // Cambios del sistema cuando no hay preferencia guardada
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const theme = localStorage.getItem('theme');
    if (!theme) {
      applyTheme(e.matches);
      const sw = document.getElementById('theme-toggle');
      if (sw) sw.checked = e.matches;
    }
  });
});
