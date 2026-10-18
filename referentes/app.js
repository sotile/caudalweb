const cases = [...document.querySelectorAll('.case')];
const search = document.querySelector('#search');
const data = window.REFERENTES || {};
let selection = new Set();
try {
  const stored = JSON.parse(localStorage.getItem('caudal-referentes') || '[]');
  if (Array.isArray(stored)) selection = new Set(stored.filter(id => cases.some(c => c.id === id && c.dataset.available === 'true')).slice(0, 3));
} catch { /* La presentación funciona sin almacenamiento disponible. */ }
let filter = 'all';
const normalize = text => text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

function applyFilters() {
  const query = normalize(search.value.trim());
  let visible = 0;
  for (const item of cases) {
    const matchesFilter = filter === 'all' || (filter === 'selected' ? selection.has(item.id) : item.dataset.region === filter);
    const show = matchesFilter && normalize(item.dataset.search).includes(query);
    item.hidden = !show;
    if (show) visible++;
  }
  document.querySelector('#results-status').textContent = `${visible} ${visible === 1 ? 'referencia visible' : 'referencias visibles'}`;
  document.querySelector('.empty').hidden = visible !== 0;
  document.querySelectorAll('.filters button').forEach(b => {
    const active = b.dataset.filter === filter;
    b.classList.toggle('active', active);
    b.setAttribute('aria-pressed', String(active));
  });
}

function renderSelection() {
  document.querySelectorAll('.selection-count').forEach(el => el.textContent = selection.size);
  document.querySelector('.selection-tray').hidden = selection.size === 0;
  document.querySelectorAll('[data-select]').forEach(button => {
    const selected = selection.has(button.dataset.select);
    button.setAttribute('aria-pressed', String(selected));
    button.textContent = selected ? '✓ Seleccionado' : '＋ Seleccionar';
    button.disabled = selection.size >= 3 && !selected;
    button.title = button.disabled ? 'Comparación de hasta tres referentes. Quitá uno para agregar otro.' : '';
  });
  try { localStorage.setItem('caudal-referentes', JSON.stringify([...selection])); } catch { /* Opcional. */ }
  if (filter === 'selected') applyFilters();
}

document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  filter = button.dataset.filter;
  applyFilters();
}));
search.addEventListener('input', applyFilters);
document.querySelectorAll('[data-select]').forEach(button => button.addEventListener('click', () => {
  const id = button.dataset.select;
  if (selection.has(id)) selection.delete(id);
  else if (selection.size < 3) selection.add(id);
  else {
    document.querySelector('#selection-status').textContent = 'Podés comparar hasta tres referentes. Quitá uno para agregar otro.';
    document.querySelector('.selection-tray').setAttribute('aria-label', 'Máximo de tres referentes. Quitá uno para agregar otro.');
    return;
  }
  document.querySelector('#selection-status').textContent = `${selection.size} referentes seleccionados`;
  renderSelection();
}));
document.querySelector('#clear-selection').addEventListener('click', () => { selection.clear(); renderSelection(); });

const imageDialog = document.querySelector('#image-dialog');
document.querySelectorAll('[data-image]').forEach(button => button.addEventListener('click', () => {
  const image = document.querySelector('#expanded-image');
  image.src = button.dataset.image;
  image.alt = button.dataset.caption;
  image.classList.toggle('mobile-image', button.dataset.image.includes('-mobile'));
  document.querySelector('#image-title').textContent = button.dataset.caption;
  imageDialog.showModal();
  imageDialog.querySelector('.image-scroll').scrollTop = 0;
}));

const compareDialog = document.querySelector('#compare-dialog');
document.querySelector('#compare-open').addEventListener('click', () => {
  const grid = document.createElement('div');
  grid.className = 'comparison-grid';
  for (const id of selection) {
    const info = data[id];
    const article = document.createElement('article');
    article.className = 'comparison-item';
    const image = document.createElement('img');
    image.src = `capturas/${id}-desktop.jpg`; image.alt = `Portada de ${info.name}`;
    const h = document.createElement('h3'); h.textContent = info.name;
    const focus = document.createElement('p'); focus.className = 'eyebrow'; focus.textContent = info.focus;
    const take = document.createElement('p'); take.textContent = info.take;
    const fit = document.createElement('small'); fit.textContent = `Propuestas relacionadas: ${info.fit}`;
    const link = document.createElement('a'); link.href = `#${id}`; link.textContent = 'Volver a la ficha ↗';
    link.addEventListener('click', () => {
      filter = 'all'; search.value = ''; applyFilters(); compareDialog.close();
    });
    article.append(image,h,focus,take,fit,link);grid.append(article);
  }
  document.querySelector('#comparison-content').replaceChildren(grid);
  compareDialog.showModal();
});

document.querySelectorAll('dialog').forEach(dialog => {
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
  });
});
document.querySelector('[data-print]').addEventListener('click', () => window.print());
renderSelection();
applyFilters();
