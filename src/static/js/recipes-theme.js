/**
 * Sistema de tema claro/oscuro
 * 
 * - Detecta la preferencia del sistema operativo
 * - Aplica el tema guardado en localStorage si existe
 * - Permite alternar el tema manualmente
 * - Sincroniza cambios automáticos del sistema si no hay preferencia guardada
 */

document.addEventListener('DOMContentLoaded', function () {

    const body = document.body;

    // Detecta si el sistema operativo tiene activado el modo oscuro
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Tema guardado previamente por el usuario
    const savedTheme = localStorage.getItem('theme');

    /**
     * Aplica el tema inicial:
     * - Si el usuario lo guardó → se respeta
     * - Si no hay guardado → se usa la preferencia del sistema
     */
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        body.classList.add('dark');
    }

    /**
     * Escucha cambios en la preferencia del sistema operativo
     * Solo se aplica si el usuario no ha definido un tema manualmente
     */
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

    /**
     * Alterna manualmente entre modo claro y oscuro
     * Guarda la preferencia del usuario en localStorage
     */
    window.toggleTheme = function () {

        body.classList.toggle('dark');

        const isDark = body.classList.contains('dark');

        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    };
});