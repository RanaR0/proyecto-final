document.addEventListener('DOMContentLoaded', function () {
    const root = document.documentElement;
    const body = document.getElementById('body');

    // Si no existe el body, evitamos ejecutar el script
    if (!body) return;

    /**
     * Aplica el tema claro u oscuro a la aplicación
     * @param {boolean} isDark - Indica si el tema debe ser oscuro
     */
    const applyTheme = (isDark) => {
        root.classList.toggle('dark', isDark);
        body.classList.toggle('dark', isDark);
    };

    // Detecta si el sistema operativo del usuario prefiere modo oscuro
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Obtiene el tema guardado previamente en localStorage
    const savedTheme = localStorage.getItem('theme');

    // Decide si se debe usar modo oscuro
    const shouldBeDark = savedTheme === 'dark' || (!savedTheme && prefersDark);

    // Aplica el tema inicial
    applyTheme(shouldBeDark);

    // Corrección de seguridad: asegura que el body tenga la clase correcta
    if (root.classList.contains('dark') && !body.classList.contains('dark')) {
        body.classList.add('dark');
    }

    /**
     * Alterna entre modo claro y oscuro manualmente
     * Guarda la preferencia en localStorage
     */
    window.toggleTheme = function () {
        const isDark = !root.classList.contains('dark');

        applyTheme(isDark);

        // Guardar preferencia del usuario
        localStorage.setItem('theme', isDark ? 'dark' : 'light');

        // Sincroniza el estado del interruptor si existe
        const toggle = document.getElementById('theme-toggle');
        if (toggle) toggle.checked = isDark;
    };

    // Establece el estado inicial del toggle (checkbox)
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
        toggle.checked = root.classList.contains('dark');
    }

    /**
     * Escucha cambios en la preferencia del sistema operativo
     * Solo se aplica si el usuario no ha elegido un tema manualmente
     */
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        const theme = localStorage.getItem('theme');

        if (!theme) {
            applyTheme(e.matches);

            const sw = document.getElementById('theme-toggle');
            if (sw) sw.checked = e.matches;
        }
    });
});