"""Genera los prototipos estáticos. Ejecutar: python3 prototipos/generar.py."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
CONCEPTS = [
    ('01-el-encuentro', 'El encuentro', 'Un hogar para muchos. Un lugar para vos.', 'Dirección principal · primarios del manual · azul #0152cd', 'encuentro'),
    ('02-casa-abierta', 'Casa abierta', 'Una bienvenida que se siente en casa.', 'Manual · hueso, noche y coral secundario', 'casa'),
    ('03-vida-para-la-ciudad', 'Vida para la Ciudad', 'La fe toma forma en lo cotidiano.', 'Manual · azul secundario y azul primario', 'ciudad'),
    ('04-tu-siguiente-paso', 'Tu siguiente paso', 'Un camino claro para cada persona.', 'Manual · azul primario, cielo y coral', 'camino'),
    ('05-esta-semana', 'Esta semana en Caudal', 'Una comunidad que sigue conectada.', 'Manual · azul secundario y cielo', 'semana'),
    ('06-un-lugar-para-vos', 'Un lugar para vos', 'Una invitación simple y memorable.', 'Manual · noche, azul primario y cielo', 'origen'),
    ('07-el-encuentro-secundarios', 'El encuentro · secundarios', 'La misma escena, con la paleta secundaria.', 'Alternativa · azul 38/109/169, cielo 125/198/224, coral 238/101/79', 'encuentro-sec'),
]

def image(name, alt, cls='', eager=False):
    return f'<img class="{cls}" src="assets/{name}" alt="{escape(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def button(label, url='#visitanos', secondary=False):
    return f'<a class="button {"secondary" if secondary else ""}" href="{url}">{label} <span aria-hidden="true">↗</span></a>'

WELCOME = 'No importa si es tu primera vez o si estás buscando un lugar para volver a empezar. Queremos conocerte y caminar con vos.'

def hero(theme):
    if theme == 'casa':
        return f'''<section class="hero hero-casa wrap"><div class="hero-copy"><p class="eyebrow">Iglesia Caudal de Vida · San Miguel</p><h1>Un hogar para muchos.<br><em>Un lugar para vos.</em></h1><p class="intro">{WELCOME}</p><div class="actions">{button('Quiero visitar Caudal')}{button('Conocé nuestra iglesia','#nosotros',True)}</div><p class="small-note">Hay un próximo paso para tu historia.</p></div><div class="photo-composition">{image('integrar.jpg','Un abrazo de bienvenida en Caudal','portrait-main',True)}{image('grupos.jpg','Jóvenes compartiendo en comunidad','portrait-small',True)}<span class="photo-caption">La vida es mejor<br>cuando la compartimos.</span></div></section>'''
    if theme in ('encuentro', 'encuentro-sec'):
        return f'''<section class="hero hero-encuentro">{image('1800x892-01.jpg','La comunidad de Caudal reunida para adorar','hero-background',True)}<div class="hero-copy wrap"><p class="eyebrow">Caudal de Vida · San Miguel</p><h1>Un hogar para muchos.<br><em>Un lugar para vos.</em></h1><p class="intro">{WELCOME}</p><div class="actions">{button('Quiero visitar Caudal')}</div></div><figure class="hero-portrait">{image('integrar.jpg','Un abrazo de bienvenida en Caudal','',True)}<figcaption>La vida es mejor cuando la compartimos.</figcaption></figure><div class="scene-caption wrap"><a href="#nosotros">Descubrí Caudal <span aria-hidden="true">↓</span></a><a class="scene-visit" href="#visitanos"><span>Nos encontramos en casa<small>España 1626 · San Miguel</small></span><b aria-hidden="true">↗</b></a></div></section>'''
    if theme == 'ciudad':
        return f'''<section class="hero hero-ciudad wrap"><div class="editorial-line"><span>UNA IGLESIA. MUCHAS HISTORIAS.</span><span>SAN MIGUEL, BUENOS AIRES</span></div><h1>Vida para<br>la <em>Ciudad.</em><span class="headline-star" aria-hidden="true">✳</span></h1><div class="editorial-bottom"><p>Creemos en una fe que se vive todos los días. Cerca de Dios, cerca de las personas, cerca de nuestra ciudad.</p>{button('Encontrá tu lugar')}</div><div class="city-photo">{image('1800x892.jpg','Personas reunidas en el auditorio de Caudal','',True)}<span>Personas reales. Una vida compartida.</span></div></section>'''
    if theme == 'camino':
        return f'''<section class="hero hero-camino wrap"><div class="hero-copy"><p class="eyebrow">Tu historia sigue creciendo</p><h1>Siempre hay<br>un <em>siguiente<br>paso.</em></h1><p class="intro">Donde estés hoy, hay un lugar para comenzar, crecer y compartir lo que Dios está haciendo en tu vida.</p>{button('Encontrá tu próximo paso','#pasos')}</div><div class="path-composition"><div class="path-start">ESTÁS ACÁ <span aria-hidden="true">↓</span></div><a class="path-card" href="#visitanos"><span>01</span><strong>Conocé Caudal</strong><span aria-hidden="true">↗</span></a>{image('integrar.jpg','Personas abrazándose en la comunidad de Caudal','path-photo',True)}<a class="path-card" href="#grupos"><span>02</span><strong>Encontrá comunidad</strong><span aria-hidden="true">↗</span></a><a class="path-card last" href="#misiones"><span>03</span><strong>Hacé la diferencia</strong><span aria-hidden="true">↗</span></a></div></section>'''
    if theme == 'semana':
        return f'''<section class="hero hero-semana wrap"><div class="week-heading"><div><p class="eyebrow">La vida de nuestra iglesia</p><h1>Esta semana,<br><em>sigamos cerca.</em></h1></div><p>Un mensaje para crecer.<br>Un lugar para encontrarnos.<br>Una comunidad para compartir.</p></div><div class="week-grid"><a class="week-main" href="#visitanos">{image('1800x892-01.jpg','Reunión de adoración en Caudal','',True)}<div><span class="eyebrow">Tu fin de semana</span><h2>Nos encontramos<br>en casa.</h2><span class="text-link">Prepará tu visita ↗</span></div></a><button class="week-message" data-video="2vUdQ47sa5c" data-title="Cuando llega Jesús — Pr. Leo Genobar">{image('mensaje-jesus.jpg','Miniatura de Cuando llega Jesús, con el Pr. Leo Genobar','',True)}<span>PARA VOLVER A ESCUCHAR</span><h3>Cuando llega Jesús</h3><span class="play-label">Ver mensaje <span aria-hidden="true">▶</span></span></button><a class="week-group" href="#grupos"><span class="eyebrow">Grupos Caudal</span><h3>La vida se<br>comparte.</h3><span aria-hidden="true">↗</span></a></div></section>'''
    return f'''<section class="hero hero-origen wrap"><p class="eyebrow">Caudal de Vida · Un lugar para vos</p><h1>La vida cambia<br>cuando la<br><em>compartimos.</em></h1><p class="origin-intro">Una fe que nos encuentra.<br>Una comunidad que nos acerca.</p><div class="actions">{button('Conocé Caudal','#historia')}{button('Planeá tu visita','#visitanos',True)}</div><a class="scroll-invitation" href="#historia">Seguí la historia <span aria-hidden="true">↓</span></a></section><section class="scroll-story" id="historia" aria-label="Conocer, compartir y transformar"><div class="story-stage"><div class="story-media"><div class="story-photo story-photo-main">{image('1800x892-01.jpg','Nuestra comunidad reunida para adorar')}</div><div class="story-photo story-photo-left">{image('integrar.jpg','Un abrazo que da la bienvenida')}</div><div class="story-photo story-photo-right">{image('grupos.jpg','Amigos compartiendo la vida')}</div></div><div class="story-shade"></div><div class="story-chapters"><div class="story-chapter"><span class="eyebrow">01 · Encontrarnos con Dios</span><h2>Todo comienza<br>con un encuentro.</h2><p>Un espacio para descubrir a Jesús y volver a empezar.</p></div><div class="story-chapter"><span class="eyebrow">02 · Compartir la vida</span><h2>De estar cerca.<br>A ser parte.</h2><p>Personas con quienes crecer, creer y caminar.</p></div><div class="story-chapter"><span class="eyebrow">03 · Vivir con propósito</span><h2>Lo que recibimos,<br>lo compartimos.</h2><p>Una iglesia presente, cerca de nuestra ciudad.</p>{button('Encontrá tu lugar','#pasos')}</div></div><div class="story-progress" aria-hidden="true"><span>ENCONTRARNOS</span><i></i><span>COMPARTIR</span><i></i><span>TRANSFORMAR</span></div></div></section>'''


def fragment(name):
    if name == 'eventos':
        try:
            from calendario import html_eventos
            live = html_eventos(ROOT)
            if live:
                return live
        except Exception as exc:
            print(f'Agenda: se mantiene la muestra ({exc}).')
    return (ROOT/'templates'/f'{name}.html').read_text()

ORDERS = {
    'casa':['bienvenida','pasos','mensajes','grupos','eventos','familia','misiones','canales','visita'],
    'encuentro':['semana','bienvenida','familia','pasos','mensajes','cultura','grupos','eventos','misiones','canales','visita'],
    'encuentro-sec':['semana','bienvenida','familia','pasos','mensajes','cultura','grupos','eventos','misiones','canales','visita'],
    'ciudad':['bienvenida','misiones','grupos','mensajes','eventos','familia','pasos','canales','visita'],
    'camino':['pasos','bienvenida','grupos','mensajes','familia','eventos','misiones','canales','visita'],
    'semana':['eventos','mensajes','grupos','bienvenida','familia','pasos','misiones','canales','visita'],
    'origen':['bienvenida','grupos','mensajes','pasos','familia','misiones','eventos','canales','visita'],
}

def document(title, body, cls=''):
    default = 'dark' if cls == 'encuentro' else 'light'
    body_class = 'encuentro encuentro-sec' if cls == 'encuentro-sec' else cls
    return f'''<!doctype html><html lang="es-AR" data-default-theme="{default}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="Propuesta de diseño para la web de la iglesia Caudal de Vida en San Miguel."><meta name="color-scheme" content="light dark"><title>{escape(title)} · Caudal de Vida</title><link rel="icon" href="assets/logo-social.jpg"><script src="../shared/theme-init.js"></script><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="refinements.css?v=20261021b"><link rel="stylesheet" href="../shared/nav.css"><script src="app.js?v=20261019b" defer></script><script src="../shared/nav.js" defer></script></head><body class="{body_class}">{body}</body></html>'''

THEME_BUTTON = '<button class="caudal-theme" type="button" data-caudal-theme aria-label="Activar modo oscuro"><span data-theme-icon aria-hidden="true">◐</span><span data-theme-label>Oscuro</span></button>'

def shell_nav(current, extra=''):
    def item(key, href, label):
        mark = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{mark}>{label}</a>'
    return (
        '<header class="caudal-nav"><a class="caudal-nav-brand" href="../index.html#slide-1" aria-label="Caudal de Vida">'
        '<img class="logo-dark" src="assets/logo-caudal-blanco.png" alt=""><img class="logo-light" src="assets/logo-caudal-negro.png" alt=""></a>'
        '<nav class="caudal-nav-links" aria-label="Presentación">'
        + item('presentacion', '../index.html#slide-1', 'Presentación')
        + item('demos', 'index.html', 'Demos')
        + f'</nav><div class="caudal-nav-tools">{extra}{THEME_BUTTON}</div></header>'
    )

BRAND_MARKUP = '<a class="brand" href="#contenido" aria-label="Caudal de Vida"><img class="brand-logo logo-dark" src="assets/logo-caudal-blanco.png" alt="Caudal de Vida"><img class="brand-logo logo-light" src="assets/logo-caudal-negro.png" alt="Caudal de Vida"></a>'
BRAND_GALLERY = '<a class="brand" href="index.html" aria-label="Caudal de Vida"><img class="brand-logo logo-dark" src="assets/logo-caudal-blanco.png" alt="Caudal de Vida"><img class="brand-logo logo-light" src="assets/logo-caudal-negro.png" alt="Caudal de Vida"></a>'

for i,(slug,name,tagline,description,theme) in enumerate(CONCEPTS):
    options=''.join(f'<option value="{s}.html" {"selected" if s==slug else ""}>{n+1:02d} · {escape(t)}</option>' for n,(s,t,*_) in enumerate(CONCEPTS))
    toolbar=shell_nav('demos', f'<label><span class="sr-only">Cambiar demo</span><select id="concept-select">{options}</select></label>')
    header=f'''<a class="skip" href="#contenido">Saltar al contenido</a>{toolbar}<header class="site-header wrap">{BRAND_MARKUP}<button class="menu-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="main-nav">Menú <span aria-hidden="true">☰</span></button><nav class="main-nav" id="main-nav" aria-label="Principal"><a href="#visitanos">Soy nuevo</a><a href="#pasos">Siguiente paso</a><a href="#grupos">Grupos</a><a href="#eventos">Eventos</a><a href="#mensajes">Mensajes</a></nav><a class="header-cta" href="#visitanos">Quiero visitar Caudal ↗</a></header>'''
    body=header+'<main id="contenido">'+hero(theme)+fragment('quick')+''.join(fragment(k) for k in ORDERS[theme])+'</main>'+fragment('footer')
    (ROOT/(slug+'.html')).write_text(document(name,body,theme))

# Compatibilidad con enlaces y marcadores anteriores
if (ROOT/'01-el-encuentro.html').exists():
    (ROOT/'02-el-encuentro.html').write_text((ROOT/'01-el-encuentro.html').read_text())
if (ROOT/'02-casa-abierta.html').exists():
    (ROOT/'01-casa-abierta.html').write_text((ROOT/'02-casa-abierta.html').read_text())

def badge(i):
    if i == 0: return '<span class="direction-badge">Dirección principal</span>'
    if i == 5: return '<span class="direction-badge">Scroll experimental</span>'
    if i == 6: return '<span class="direction-badge">Secundarios del manual</span>'
    return ''

cards=''.join(f'''<article class="concept-card preview-{t}"><a class="concept-preview" href="{s}.html"><img src="previews/{s}-light.jpg" data-preview-light="previews/{s}-light.jpg" data-preview-dark="previews/{s}-dark.jpg" alt="Vista de la propuesta {escape(n)}" loading="lazy"><span class="preview-number">{i+1:02d}</span><span class="preview-word">{escape(n)}</span>{badge(i)}</a><div class="concept-details"><span class="eyebrow">Propuesta {i+1:02d}</span><h2><a href="{s}.html">{escape(n)} <span aria-hidden="true">↗</span></a></h2><p>{escape(tag)}</p><small>{escape(d)}</small><div class="theme-links"><a href="{s}.html?theme=light">☀ Versión clara ↗</a><a href="{s}.html?theme=dark">◐ Versión oscura ↗</a></div></div></article>''' for i,(s,n,tag,d,t) in enumerate(CONCEPTS))
gallery=f'''{shell_nav('demos')}<main class="gallery wrap"><div class="gallery-intro"><p class="eyebrow">Demos</p><h1>Elegí una<br><em>dirección.</em></h1><p>Siete versiones de la misma iglesia. El encuentro usa los colores principales. La 07 usa los secundarios.</p></div><div class="concept-grid">{cards}</div><section class="gallery-notes"><p>Fotografías de Caudal. La agenda es de muestra. Horarios y contactos se confirman antes de publicar.</p></section><footer class="gallery-footer">Caudal de Vida · Prototipos locales para revisión · Octubre de 2026</footer></main>'''
(ROOT/'index.html').write_text(document('Propuestas para el inicio',gallery,'gallery-page'))
print('Generados: galería y prototipos HTML.')
