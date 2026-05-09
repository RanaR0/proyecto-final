/**
 * Sistema de cambio de tema (claro/oscuro)
 * 
 * - Detecta la preferencia del sistema operativo
 * - Aplica el tema guardado en localStorage si existe
 * - Permite alternar entre modo claro y oscuro manualmente
 * - Sincroniza el estado con el checkbox de la UI
 */

document.addEventListener('DOMContentLoaded', function () {

  // Referencias a elementos del DOM
  const body = document.body;
  const themeToggle = document.getElementById('theme-toggle');

  // Detecta si el usuario tiene preferencia de modo oscuro en el sistema
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  // Tema guardado previamente en localStorage
  const savedTheme = localStorage.getItem('theme');

  /**
   * Determina si el tema inicial debe ser oscuro:
   * - Si el usuario lo guardó explícitamente
   * - O si no hay preferencia guardada y el sistema es oscuro
   */
  const shouldBeDark = savedTheme === 'dark' || (!savedTheme && prefersDark);

  // Aplica tema oscuro si corresponde
  if (shouldBeDark) {
    body.classList.add('dark');
    if (themeToggle) themeToggle.checked = true;
  }

  /**
   * Escucha cambios en la preferencia del sistema operativo
   * Solo se aplica si el usuario NO ha elegido un tema manualmente
   */
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {

    const theme = localStorage.getItem('theme');

    // Solo actuar si el usuario no ha fijado un tema manual
    if (!theme) {
      if (e.matches) {
        body.classList.add('dark');
        if (themeToggle) themeToggle.checked = true;
      } else {
        body.classList.remove('dark');
        if (themeToggle) themeToggle.checked = false;
      }
    }
  });

  /**
   * Alterna manualmente entre modo claro y oscuro
   * Guarda la preferencia en localStorage
   */
  window.toggleTheme = function () {

    body.classList.toggle('dark');

    const isDark = body.classList.contains('dark');

    // Guarda preferencia del usuario
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Sincroniza estado del checkbox con el tema actual
    if (themeToggle) {
      themeToggle.checked = isDark;
    }
  };
});