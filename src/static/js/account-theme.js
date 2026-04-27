document.addEventListener('DOMContentLoaded', function () {
    const body = document.getElementById('body');

    if (!body) return;

    // Detectar preferencia del sistema
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        body.classList.add('dark');
    }

    // Función para toggle
    window.toggleTheme = function () {
        body.classList.toggle('dark');
        const isDark = body.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        // Update toggle if exists
        const toggle = document.getElementById('theme-toggle');
        if (toggle) toggle.checked = isDark;
    }

    // Set initial state for toggle
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
        toggle.checked = body.classList.contains('dark');
    }
});
