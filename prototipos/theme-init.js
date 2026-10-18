// Se ejecuta antes del CSS para evitar destellos al recuperar la preferencia.
(() => {
  const allowed = ['light', 'dark'];
  const requested = new URLSearchParams(location.search).get('theme');
  let saved;
  try { saved = localStorage.getItem('caudal-theme'); } catch { /* Navegación local sin almacenamiento. */ }
  const theme = allowed.includes(requested) ? requested : allowed.includes(saved) ? saved : document.documentElement.dataset.defaultTheme || 'light';
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
})();
