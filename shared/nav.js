(() => {
  // Asegurar que no quede ningún enlace a referentes en la navegación
  document.querySelectorAll('.caudal-nav a[href*="referentes"]').forEach((el) => el.remove());

  const paint = (theme) => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.style.colorScheme = theme;
    document.querySelectorAll('[data-caudal-theme]').forEach((button) => {
      const dark = theme === 'dark';
      button.setAttribute('aria-pressed', String(dark));
      button.setAttribute('aria-label', dark ? 'Activar modo claro' : 'Activar modo oscuro');
      const label = button.querySelector('[data-theme-label]');
      const icon = button.querySelector('[data-theme-icon]');
      if (label) label.textContent = dark ? 'Claro' : 'Oscuro';
      if (icon) icon.textContent = dark ? '☀' : '◐';
    });
  };

  paint(document.documentElement.dataset.theme || document.documentElement.getAttribute('data-theme') || 'dark');

  document.querySelectorAll('[data-caudal-theme]').forEach((button) => {
    button.addEventListener('click', () => {
      const current = document.documentElement.dataset.theme || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('caudal-theme', next); } catch { /* Opcional. */ }
      paint(next);
    });
  });
})();
