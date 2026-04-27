document.addEventListener('DOMContentLoaded', function () {
  const body = document.body;

  // Detectar preferencia del sistema
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('theme');

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    body.classList.add('dark');
  }

  // Escuchar cambios en la preferencia del sistema
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const theme = localStorage.getItem('theme');
    if (!theme) {
      if (e.matches) {
        body.classList.add('dark');
      } else {
        body.classList.remove('dark');
      }
    }
  });

  /* Función para toggle tema (opcional) */
  window.toggleTheme = function () {
    body.classList.toggle('dark');
    const isDark = body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }
});
