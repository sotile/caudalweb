(() => {
  const allowed = ['light', 'dark'];
  const requested = new URLSearchParams(location.search).get('theme');
  let saved = '';
  try {
    saved = localStorage.getItem('caudal-theme') || localStorage.getItem('caudal-deck-theme') || '';
  } catch { /* La vista también funciona sin almacenamiento. */ }
  const fallback = document.documentElement.dataset.defaultTheme || document.documentElement.getAttribute('data-theme') || 'dark';
  const theme = allowed.includes(requested) ? requested : allowed.includes(saved) ? saved : fallback;
  document.documentElement.dataset.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  document.documentElement.style.colorScheme = theme;
  try { localStorage.setItem('caudal-theme', theme); } catch { /* Opcional. */ }
})();
