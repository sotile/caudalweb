document.querySelector('#concept-select')?.addEventListener('change', (event) => {
  window.location.href = event.target.value + '?theme=' + document.documentElement.dataset.theme;
});

const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
const closeMenu = () => {
  toggle?.setAttribute('aria-expanded', 'false');
  nav?.classList.remove('is-open');
};
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeMenu();
});

const dialog = document.querySelector('.video-dialog');
document.querySelectorAll('[data-video]').forEach(button => {
  button.addEventListener('click', () => {
    const id = button.dataset.video;
    if (!/^[a-zA-Z0-9_-]{11}$/.test(id)) return;
    const title = button.dataset.title || 'Mensaje de Caudal';
    document.querySelector('#video-title').textContent = title;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&playsinline=1&rel=0`;
    iframe.title = title;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    dialog.querySelector('.video-container').replaceChildren(iframe);
    dialog.querySelector('.video-external').href = `https://www.youtube.com/watch?v=${id}`;
    dialog.showModal();
  });
});
dialog?.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
dialog?.addEventListener('close', () => dialog.querySelector('.video-container').replaceChildren());
const cultura = document.querySelector('[data-cultura]');
if (cultura) {
  const frame = cultura.querySelector('[data-cultura-frame]');
  const tracks = [...cultura.querySelectorAll('[data-track]')];
  const playCultura = button => {
    const id = button.dataset.track;
    if (!/^[a-zA-Z0-9_-]{11}$/.test(id)) return;
    const title = button.dataset.title || 'Cultura Music';
    tracks.forEach(item => {
      if (!item.closest('.cultura-tracks')) return;
      if (item.dataset.track === id) item.setAttribute('aria-current', 'true');
      else item.removeAttribute('aria-current');
    });
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&playsinline=1&rel=0`;
    iframe.title = title;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.replaceChildren(iframe);
  };
  tracks.forEach(button => button.addEventListener('click', () => playCultura(button)));
}

dialog?.addEventListener('click', event => {
  if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }
});

// Las dos paletas se conservan al pasar de una propuesta a otra.
const themeButtons = document.querySelectorAll('.theme-toggle');
function applyTheme(theme, persist = false) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  if (persist) {
    try { localStorage.setItem('caudal-theme', theme); } catch { /* La vista también funciona sin localStorage. */ }
    const url = new URL(location.href);
    url.searchParams.set('theme', theme);
    try { history.replaceState(null, '', url); } catch { /* Compatible con archivos locales. */ }
  }
  themeButtons.forEach(button => {
    button.setAttribute('aria-pressed', String(theme === 'dark'));
    button.setAttribute('aria-label', `Activar modo ${theme === 'dark' ? 'claro' : 'oscuro'}`);
    button.querySelector('[data-theme-label]').textContent = theme === 'dark' ? 'Claro' : 'Oscuro';
    button.querySelector('[data-theme-icon]').textContent = theme === 'dark' ? '☀' : '◐';
  });
  document.querySelectorAll('[data-preview-light]').forEach(img => {
    img.src = theme === 'dark' ? img.dataset.previewDark : img.dataset.previewLight;
  });
}
applyTheme(document.documentElement.dataset.theme || 'light');
themeButtons.forEach(button => button.addEventListener('click', () => {
  applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark', true);
}));

// Relato ligado al scroll nativo: un solo frame pendiente, sin capturar rueda ni gestos.
const story = document.querySelector('.scroll-story');
if (story) {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const compact = matchMedia('(max-width: 760px)');
  const chapters = [...story.querySelectorAll('.story-chapter')];
  const photos = story.querySelector('.story-media');
  let scheduled = false;
  const clamp = value => Math.max(0, Math.min(1, value));
  function paintStory() {
    scheduled = false;
    const active = !reduceMotion.matches && !compact.matches;
    story.classList.toggle('motion-enabled', active);
    if (!active) {
      story.style.removeProperty('--story-p');
      photos.style.transform = '';
      chapters.forEach(chapter => {
        chapter.style.opacity = '';
        chapter.style.transform = '';
        chapter.style.visibility = '';
        chapter.inert = false;
      });
      return;
    }
    const box = story.getBoundingClientRect();
    const p = clamp(-box.top / Math.max(1, box.height - innerHeight));
    story.style.setProperty('--story-p', p.toFixed(4));
    chapters.forEach((chapter, i) => {
      const start = i / 3;
      const fadeIn = i === 0 ? 1 : clamp((p - start) / 0.08);
      const fadeOut = i === 2 ? 1 : 1 - clamp((p - start - 0.25) / 0.083);
      const opacity = Math.min(fadeIn, fadeOut);
      chapter.style.opacity = opacity.toFixed(3);
      chapter.style.transform = `translateY(${(i - p * 2.6) * 55}px)`;
      chapter.style.visibility = opacity > 0.03 ? 'visible' : 'hidden';
      chapter.inert = opacity < 0.5;
    });
  }
  function scheduleStory() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(paintStory); }
  }
  addEventListener('scroll', scheduleStory, {passive:true});
  addEventListener('resize', scheduleStory);
  reduceMotion.addEventListener('change', scheduleStory);
  compact.addEventListener('change', scheduleStory);
  paintStory();
}
