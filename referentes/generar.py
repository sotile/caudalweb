"""Genera el dossier local a partir de capturas y fichas editoriales verificadas."""
from pathlib import Path
from html import escape as e
from urllib.parse import urlsplit
import json

ROOT = Path(__file__).parent
DATE = '17 de octubre de 2026'
ORDER = ['life','elevation','saddleback','hillsong','bethel','passion','ieb-cordoba','rey-jesus','adoracion','centro-adoracion','rincon','missio']
CASES = {
 'life': dict(place='Estados Unidos',focus='Bienvenida y próximo paso',tags=['Bienvenida','Comunidad','Contenido'],
  thesis='Una campaña puede ocupar la portada sin perder el recorrido de bienvenida.',
  aesthetic='La captura presenta una campaña estacional: fondo rosado claro, verde, naranja y letras gruesas de tono amable. Más abajo aparecen fotografías de familias y comunidad. La estética de esta campaña no representa necesariamente todas las páginas permanentes.',
  functions=['Elección de sede y acceso a participación en línea.','Accesos a oración, grupos y primera visita.','Biblioteca multimedia y presentación de espacios para niños.'],
  reach='La web conecta sedes físicas, participación en línea, recursos y redes. El canal enlazado corresponde a Life.Church; la cifra no agrega canales musicales ni otros productos.',
  take='Conservar una bienvenida permanente y una campaña temporal bien delimitada. Para Caudal: banner actualizable y accesos rápidos a visitar, grupos y oración.',
  caution='Una campaña visual grande necesita una alternativa permanente cuando no haya actividad destacada.',
  fit='Casa abierta + Esta semana en Caudal',links=[('Canal institucional','https://www.youtube.com/user/LifeChurchtv')]),
 'elevation': dict(place='Estados Unidos',focus='Mensajes y participación',tags=['Contenido','Comunidad','Eventos'],
  thesis='El contenido semanal funciona como entrada a la vida de la iglesia.',
  aesthetic='Base negra y gris, tipografía sans serif, acento naranja en la marca y botones blancos redondeados. Hero audiovisual inmersivo con video y fotografía de adoración comunitaria, buscador superior y llamados directos a conectarse.',
  functions=['Mensaje reciente con acceso a su reproducción.','Recorridos presenciales, streaming y encuentros comunitarios.','Grupos, servicio, eventos y espacios para familias.'],
  reach='Integra comunidad presencial y digital, mensajes, música y formación. La cifra corresponde a Elevation Church, no al canal Elevation Worship.',
  take='Una biblioteca viva desde YouTube y acciones claras después de ver un mensaje. Para Caudal: mensaje destacado, series y siguiente paso.',
  caution='Elevation sostiene una producción audiovisual constante; para Caudal conviene asegurar que la portada funcione igual de bien con una imagen fija o un video liviano.',
  fit='El encuentro + Esta semana en Caudal',links=[('Canal institucional','https://www.youtube.com/@elevationchurch')]),
 'saddleback': dict(place='Estados Unidos · versión en español observada',focus='Navegación por intención',tags=['Bienvenida','Comunidad','Formación'],
  thesis='La persona elige lo que necesita sin aprender la estructura interna de la iglesia.',
  aesthetic='Fondos blancos y gris claro, azul como acento, fotografías grandes y tarjetas con esquinas suaves. La portada yuxtapone el último mensaje y una columna de acciones personales. En esta sesión el sitio redirigió a su versión en español.',
  functions=['Accesos explícitos para primera visita, fe, bautismo, comunidad y servicio.','Mensaje reciente y contenido de podcast.','Ubicaciones, acompañamiento, grupos y aplicación.'],
  reach='La portada presenta sedes en distintas regiones y comunidad en línea. Las funciones observadas muestran variedad de canales; no prueban una tasa de conversión o participación.',
  take='Organizar Siguiente paso por necesidades y verbos. Para Caudal: Soy nuevo, conocer a Jesús, bautismo, grupos y servir con destinos propios.',
  caution='Adoptar la claridad de los recorridos y reducir la cantidad de opciones al equipo que podrá acompañarlas.',
  fit='Tu siguiente paso',links=[('Canal institucional','https://www.youtube.com/saddlebackchurch')]),
 'hillsong': dict(place='Red global · portada internacional',focus='Marca y ecosistema',tags=['Bienvenida','Formación','Música'],
  thesis='Una identidad compartida conecta comunidad, música y educación.',
  aesthetic='Cabecera blanca con navegación en dos niveles, marca monocroma y un primer bloque audiovisual de gran tamaño. La bienvenida es breve. Música, conferencias y formación tienen presencia dentro de una arquitectura de alcance global.',
  functions=['Búsqueda de iglesia por ubicación.','Acceso a sedes, participación en línea y distintos idiomas.','Música, College, conferencias e historias.'],
  reach='Su ecosistema incluye canales regionales y musicales. Se mide aquí el canal Hillsong Church enlazado desde la portada, sin sumarlo a Worship, UNITED o Young & Free.',
  take='Compartir criterios de identidad entre Caudal e Instituto Cultura conservando recorridos y públicos específicos.',
  caution='Una portada global resuelve necesidades distintas de una iglesia local. En Caudal, dirección y primera visita deben estar más cerca.',
  fit='El encuentro + Un lugar para vos',links=[('Canal institucional','https://www.youtube.com/hillsong'),('Hillsong Buenos Aires','https://hillsong.com/argentina/buenosaires/')]),
 'bethel': dict(place='Redding, Estados Unidos',focus='Identidad editorial y formación',tags=['Formación','Música','Eventos'],
  thesis='La iglesia presenta sus ministerios y escuelas como un ecosistema coherente.',
  aesthetic='Hero audiovisual de reunión, cabecera negra, letras blancas y un titular serif de gran escala. Conviven una expresión editorial más solemne y una navegación funcional. Los accesos presencial y en línea aparecen juntos.',
  functions=['Acceso a participación presencial y digital.','Calendario, ministerios y distintas vías de acompañamiento.','Música, escuelas, recursos y suscripción a novedades.'],
  reach='La portada enlaza Bethel Online, escuelas, música y recursos. La métrica pertenece al canal Bethel; no se agrega el alcance de Bethel Music.',
  take='Usar tipografía editorial con fotografía real y hacer visible la formación. Para Caudal: una presentación clara de Instituto Cultura.',
  caution='La experiencia depende de buenos materiales audiovisuales; las necesidades prácticas deben funcionar también con una imagen estática.',
  fit='Un lugar para vos + El encuentro',links=[('Canal institucional','https://www.youtube.com/user/ibetheltv')]),
 'passion': dict(place='Atlanta y Washington DC, Estados Unidos',focus='Misión y territorio',tags=['Bienvenida','Comunidad','Formación'],
  thesis='Una frase de misión organiza la primera impresión y sitúa a la iglesia en su ciudad.',
  aesthetic='Gran escena audiovisual dentro de un marco redondeado, títulos blancos contundentes y botones cian. La jerarquía se apoya en tipografía de mucho peso, espacios amplios y navegación por ubicaciones.',
  functions=['Selección de ciudad o sede.','Eventos destacados y presentación del liderazgo.','Passion Equip, recursos y suscripción a novedades.'],
  reach='Conecta la iglesia con un movimiento de conferencias, formación y recursos. La cifra se limita a Passion City Church, sin sumar Passion Conferences ni proyectos musicales.',
  take='Convertir Vida para la Ciudad en un concepto visible, ligado a personas y acciones concretas de San Miguel.',
  caution='Equilibrar la declaración de misión con una acción inmediata para quien visita por primera vez.',
  fit='Vida para la Ciudad + El encuentro',links=[('Canal institucional','https://www.youtube.com/@passioncitychurch')]),
 'rincon': dict(place='Argentina · referencia aportada para Córdoba',focus='Recursos y continuidad semanal',tags=['Contenido','Comunidad'],
  thesis='Revista, podcast y transmisión amplían la relación más allá de una reunión.',
  aesthetic='Gráficas de campaña saturadas con azul, violeta y naranja; textos integrados en imágenes y una composición más densa. La captura muestra una solicitud de notificaciones sobre el primer bloque, que forma parte de la experiencia observada.',
  functions=['Accesos a revista, podcast y sermones en línea.','Navegación institucional, contacto y área de miembros.','Enlaces a Facebook e Instagram y solicitud de notificaciones.'],
  reach='Se observan dos redes y varios formatos propios. No se identificó un canal de YouTube en la portada capturada; no se atribuye una cifra de seguidores ni engagement.',
  take='Aprovechar material existente para sostener la semana: mensajes, artículos o series. El podcast de Caudal puede incorporarse cuando se defina su fuente.',
  caution='En Caudal conviene priorizar lectura móvil, textos en HTML y una bienvenida libre de pedidos de notificaciones al ingresar.',
  fit='Esta semana en Caudal',links=[('Instagram institucional','https://www.instagram.com/iglesiarincon/'),('Facebook institucional','https://www.facebook.com/iglesiarincon/')]),
 'missio': dict(place='Córdoba, Argentina · dominio corregido',focus='Predicación y recursos existentes',tags=['Contenido','Música','Formación'],
  thesis='Una iglesia local puede reunir sus canales y recursos en un sitio de estructura simple.',
  aesthetic='Cabecera blanca centrada, fotografía urbana en el bloque principal, un titular serif dentro de la pieza visual y acentos dorados. El contenido posterior alterna explicación institucional, predicación y recursos.',
  functions=['Predicación destacada mediante contenido incrustado de Spotify.','Accesos a sermones, música y contenidos de ministerios.','Formación, contacto, horario y ubicación.'],
  reach='La web enlaza varios canales y ministerios. La cifra seleccionada corresponde al canal de predicaciones de Missio Córdoba; no suma Es Hora de Ser Real ni otras congregaciones.',
  take='Integrar contenido publicado en las plataformas que la iglesia ya utiliza. Para Caudal: YouTube, reels seleccionados y formación.',
  caution='Se corrigió el dominio aportado. Mantener horarios y próxima acción por encima de textos institucionales extensos.',
  fit='Esta semana en Caudal + Vida para la Ciudad',links=[('Canal de predicaciones de Córdoba','https://www.youtube.com/@iglesiacristianamissiocord873/videos')]),
}


CASES.update({
 'rey-jesus': dict(place='Palermo, CABA · José A. Cabrera 4656',focus='Bienvenida y participación local',tags=['Bienvenida','Comunidad'],
  thesis='Dos acciones inmediatas orientan la primera visita: horarios y bienvenida.',
  aesthetic='Foto de reunión con filtro oscuro azulado, título blanco condensado de gran tamaño y acento cian. Las tarjetas inferiores alternan fondos claros y oscuros. La cabecera reúne navegación, redes y selector de apariencia.',
  functions=['Horarios, mapa y acceso para nuevos visitantes.','Pedidos de oración por WhatsApp y opciones de donación.','Ministerios por etapas y formulario externo para grupos.'],
  reach='La portada conecta redes, grupos y contacto. No se atribuye una cifra de audiencia. El sitio identifica la iglesia de Palermo; no confirma la denominación bautista de la lista original.',
  take='Dar prioridad a horarios y primera visita; acompañar cada ministerio con una acción concreta.',
  caution='Revisar la identidad de cada referencia. La ubicación coincide con Palermo, pero la afiliación aportada queda sin confirmar.',
  fit='Casa abierta + Tu siguiente paso',links=[]),
 'centro-adoracion': dict(place='Villa Sarmiento, Buenos Aires · Ministerio Altares',focus='Comunidad, formación y acción social',tags=['Comunidad','Formación','Contenido'],
  thesis='Una página extensa reúne comunidad, enseñanza y ayuda social.',
  aesthetic='Cabecera blanca, marca azul y títulos negros gruesos; fotografía de adoración con texto serif superpuesto. La página realizada en Canva sigue una secuencia larga de bloques visuales.',
  functions=['Navegación a actividades, iglesia virtual y galerías.','Enlaces a transmisiones, podcast y música.','Formación, fundación y datos de ubicación.'],
  reach='La página identifica Ministerio Altares y una sede en Villa Sarmiento. Ofrece varios canales sin métricas verificadas. El nombre genérico de la lista no permite asegurar que esta fuera la iglesia inicialmente pretendida.',
  take='Mostrar el trabajo social y reunir canales existentes con accesos fáciles de mantener.',
  caution='La lectura móvil de piezas con texto necesita revisión. Para Caudal, usar textos HTML y una agenda con fechas claras.',
  fit='Vida para la Ciudad + Esta semana en Caudal',links=[]),
 'ieb-cordoba': dict(place='Córdoba, España · referencia confirmada por el cliente',focus='Mensajes y vida semanal',tags=['Contenido','Bienvenida','Comunidad'],
  thesis='El contenido reciente conecta la bienvenida con la vida semanal.',
  aesthetic='Video de fondo, cabecera superpuesta, letras blancas de gran tamaño y botones verdes. Debajo aparecen bloques claros y accesos a mensajes, agenda y noticias.',
  functions=['Horario de reunión visible en el primer bloque.','Mensajes recientes y acceso a su archivo.','Agenda, noticias, presentación institucional y contacto.'],
  reach='La portada enlaza su canal de YouTube. El pie identifica Calle Vicente Aleixandre 4, Córdoba, España. No se asigna una cifra de audiencia sin verificarla.',
  take='Mostrar horario y mensaje reciente con accesos claros a la agenda.',
  caution='Prever imagen alternativa al video y revisar contraste y legibilidad móvil.',
  fit='Esta semana en Caudal + Casa abierta',links=[('Canal institucional','https://www.youtube.com/iebcordoba'),('Contacto y reuniones','https://iebcordoba.es/contacto/')]),
})

PENDING = {
 'ieb-cordoba':('Córdoba, España · referencia confirmada','URL confirmada por el cliente: https://iebcordoba.es/.'),
 'rey-jesus':('Palermo, Buenos Aires · dato aportado','Confirmar el dominio actual de la congregación. No se mezcla con iglesias homónimas de otros países.'),
 'adoracion':('Buenos Aires · dato aportado','No se identificó de forma fiable la congregación de Buenos Aires. El sitio adoracion.co declara su sede en Barranquilla, Colombia; se descarta como reemplazo de esta referencia argentina.'),
 'centro-adoracion':('Buenos Aires · dato aportado','Confirmar identidad y dominio; el nombre por sí solo no permite elegir una congregación homónima.'),
}

def links(items):
    return ''.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)} <span aria-hidden="true">↗</span></a>' for t,u in items)

def picture(id, mode='desktop', label='Ampliar captura'):
    return f'<button class="capture" data-image="capturas/{id}-{mode}.jpg" data-caption="{e(label)}"><img src="capturas/{id}-{mode}.jpg" alt="{e(label)}" loading="lazy" width="1440" height="1000"><span class="capture-zoom">{e(label)} ⤢</span></button>'

def card(id, index, captured, metric):
    title=captured['name'];good=captured['available']
    info=CASES.get(id,{})
    tags=info.get('tags',[])
    tags_html=''.join(f'<span class="tag">{e(t)}</span>' for t in tags)
    status=captured.get('captureLabel','Portada capturada') if good else 'Enlace pendiente'
    badge=f'<span class="status {"ok" if good else "pending"}"><i></i>{status}</span>'
    button=f'<button class="choose" data-select="{id}" aria-pressed="false">＋ Seleccionar</button>' if good else ''
    group='Mundo' if captured['region']=='Mundo' else 'Argentina'
    place=info.get('place',PENDING.get(id,('',''))[0])
    headline=f'<div class="case-title"><div><p class="eyebrow">{index:02d} / {group} · {e(place)}</p><h2>{e(title)}</h2></div><div class="case-actions">{badge}{button}</div></div>'
    if not good:
        place,note=PENDING[id]
        return f'''<article class="case pending-case" id="{id}" data-region="Argentina" data-available="false" data-search="{e(title.lower())}">{headline}<div class="pending-layout"><div class="pending-visual"><span class="pending-symbol" aria-hidden="true">↗</span><strong>Captura del inicio pendiente</strong><span>{e(urlsplit(original_url(id)).netloc)}</span></div><div><h3>Primero, validar el enlace.</h3><p>La dirección aportada no resolvió en la comprobación del {DATE}. No se pudo observar su portada ni verificar la identidad del sitio.</p><p>{e(note)}</p><p class="muted">Esta condición no demuestra que la iglesia carezca de web o presencia digital. La estética, las funciones y el alcance quedan sin evaluar.</p><div class="source-links">{links([('Dirección aportada',original_url(id))])}</div><button class="evidence" data-image="capturas/{id}-desktop.jpg" data-caption="Evidencia del intento de consulta; no es una captura del sitio de la iglesia">Ver evidencia de consulta ⤢</button></div></div></article>'''
    m=metric or {}
    if m.get('verified'):
        metric_html=f'<div class="metric"><span class="metric-label">YouTube · canal identificado</span><strong>{e(m["subscriberLabel"])}</strong><a href="{e(m["url"])}" target="_blank" rel="noopener">{e(m["title"])} ↗</a><small>Lectura pública redondeada · {DATE}</small></div>'
    else:
        metric_html='<div class="metric unmeasured"><span class="metric-label">Alcance cuantitativo</span><strong>Sin cifra validada</strong><small>No se infiere audiencia por apariencia, tamaño de iglesia o cantidad de canales.</small></div>'
    styles=captured.get('styles',{})
    typo=styles.get('font','No registrada').replace('"','')
    urls=[('Sitio consultado',captured['url'])]+info['links']
    capture_note='Captura de escritorio · 1440 × 1000 · '+DATE
    if id=='elevation':capture_note+=' · recurso visual principal incompleto en esta sesión'
    if id=='saddleback':capture_note+=' · versión /es/'
    if captured.get('providedURL'):capture_note+=' · URL aportada sustituida por dominio institucional identificado'
    features=''.join(f'<li>{e(x)}</li>' for x in info['functions'])
    mobile=f'<button data-image="capturas/{id}-mobile.jpg" data-caption="{e(title)} · vista móvil 390 × 844">Vista móvil ⤢</button>'
    full=f'<button data-image="capturas/{id}-completa.jpg" data-caption="{e(title)} · recorrido ampliado del inicio, hasta 11.000 px">Inicio ampliado ⤢</button>'
    corrected=f'<p class="correction">Dominio aportado: <span>{e(captured["providedURL"])}</span>. {e(captured.get('identityNote','Se utiliza el dominio institucional identificado para la congregación de Córdoba.'))}</p>' if captured.get('providedURL') else ''
    return f'''<article class="case" id="{id}" data-region="{group}" data-available="true" data-search="{e((title+' '+' '.join(tags)).lower())}">{headline}<div class="case-top"><div class="capture-panel">{picture(id,label=title+' · inicio de escritorio')}<p class="capture-note">{e(capture_note)}</p><div class="view-links">{mobile}{full}<a href="{e(captured['url'])}" target="_blank" rel="noopener">Visitar web ↗</a></div></div><div class="case-summary"><span class="focus-label">{e(info['focus'])}</span><h3>{e(info['thesis'])}</h3><div class="tags">{tags_html}</div>{metric_html}<dl><div><dt>Tipografía CSS declarada</dt><dd>{e(typo)}</dd></div><div><dt>Relación con nuestras propuestas</dt><dd>{e(info['fit'])}</dd></div></dl></div></div><div class="case-analysis"><section><h4>01 · Estética observada</h4><p>{e(info['aesthetic'])}</p></section><section><h4>02 · Funcionalidad visible</h4><ul>{features}</ul></section><section><h4>03 · Presencia digital</h4><p>{e(info['reach'])}</p></section></div><div class="case-conclusion"><section><h4>Qué llevaríamos a Caudal</h4><p>{e(info['take'])}</p></section><section><h4>Qué conviene resolver con criterio propio</h4><p>{e(info['caution'])}</p></section></div>{corrected}<div class="sources"><span>Fuentes y contexto</span><div class="source-links">{links(urls)}</div><small>Lectura de diseño y arquitectura del inicio. No constituye una auditoría de accesibilidad, rendimiento, conversión o tecnología de backend.</small></div></article>'''

def original_url(id):
    return {'ieb-cordoba':'https://www.iebcordoba.org/','rey-jesus':'https://elreyjesus.org.ar/','adoracion':'https://iglesiaadoracion.org/','centro-adoracion':'https://centrodeadoracion.org/'}[id]

def main():
    records={id:json.loads((ROOT/'datos'/f'{id}.json').read_text()) for id in ORDER}
    metrics={d['id']:d for d in json.loads((ROOT/'datos'/'alcance.json').read_text())}
    count=sum(d['available'] for d in records.values())
    world_count=sum(d['region']=='Mundo' for d in records.values())
    argentina_count=len(records)-world_count
    cards=''.join(card(id,i+1,records[id],metrics.get(id)) for i,id in enumerate(ORDER))
    jump=''.join(f'<a href="#{id}">{e(records[id]["name"])}</a>' for id in ORDER if records[id]['available'])
    manifest={id:{'name':records[id]['name'],'region':records[id]['region'],'focus':CASES.get(id,{}).get('focus','Pendiente'),'take':CASES.get(id,{}).get('take','Sin evaluación'),'fit':CASES.get(id,{}).get('fit','—')} for id in ORDER}
    (ROOT/'seleccion.js').write_text('window.REFERENTES = '+json.dumps(manifest,ensure_ascii=False)+';\n')
    html=f'''<!doctype html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="Dossier de referencias de diseño y experiencia digital para Caudal de Vida, con capturas reales y fichas comparativas."><title>Referentes digitales · Caudal de Vida</title><link rel="stylesheet" href="styles.css"><script src="seleccion.js" defer></script><script src="app.js" defer></script></head><body><a class="skip" href="#referencias">Saltar a las fichas</a><header class="topbar"><a class="brand" href="#inicio"><span class="brand-icon">CV</span><span>CAUDAL DE VIDA<small>Dirección creativa y estrategia web</small></span></a><nav aria-label="Dossier"><a href="#referencias">Referentes</a><a href="#criterios">Criterios</a><a href="../prototipos/index.html">Nuestras propuestas ↗</a></nav><button class="print-button" data-print>Imprimir / PDF ↗</button></header><main><section class="cover wrap" id="inicio"><div class="cover-label"><p class="eyebrow">Dossier para presentación al cliente</p><span>Octubre 2026 / Diego</span></div><h1>Mirar afuera.<br>Encontrar <em>nuestra forma.</em></h1><div class="cover-bottom"><p>Una selección de experiencias digitales de iglesias para conversar sobre bienvenida, identidad, contenido y comunidad. Capturas reales y aprendizajes concretos para la nueva web de Caudal de Vida.</p><a class="primary" href="../prototipos/index.html">Ver las seis propuestas de Caudal <span>↗</span></a></div><div class="numbers"><div><strong>12</strong><span>Referencias aportadas</span></div><div><strong>{count:02d}</strong><span>Sitios / portales capturados</span></div><div><strong>{12-count:02d}</strong><span>Sin captura identificada</span></div><div><strong>06</strong><span>Propuestas propias</span></div></div><div class="cover-note"><span class="note-mark">i</span><p>La selección no es un ranking. Las capturas muestran el estado de cada sitio en la fecha de consulta; las cifras corresponden a canales específicos, no a visitas de la web ni a tamaño de congregación.</p></div></section><section class="method wrap" id="criterios"><div><p class="eyebrow">Cómo leer este dossier</p><h2>Cuatro preguntas<br>para mirar con criterio.</h2></div><div class="method-grid"><div><span>01</span><h3>¿Qué se siente?</h3><p>Fotografía, tipografía, composición y tono de bienvenida.</p></div><div><span>02</span><h3>¿Qué se puede hacer?</h3><p>Visitar, ver un mensaje, encontrar comunidad y participar.</p></div><div><span>03</span><h3>¿Cómo se sostiene?</h3><p>Contenido semanal, formatos y ecosistema de canales.</p></div><div><span>04</span><h3>¿Qué sirve a Caudal?</h3><p>Ideas aplicables a nuestra identidad, equipo y herramientas.</p></div></div></section><section class="reference-section wrap" id="referencias"><div class="reference-heading"><div><p class="eyebrow">Internacionales y Argentina</p><h2>Las referencias,<br><em>en detalle.</em></h2></div><p>Ampliá las capturas, explorá la vista móvil<br>y seleccioná los casos para discutir.</p></div><div class="filterbar"><div class="filters" role="group" aria-label="Filtrar referentes"><button class="active" data-filter="all" aria-pressed="true">Todos <span>12</span></button><button data-filter="Mundo" aria-pressed="false">Mundo <span>{world_count}</span></button><button data-filter="Argentina" aria-pressed="false">Argentina <span>{argentina_count}</span></button><button data-filter="selected" aria-pressed="false">Mi selección <span class="selection-count">0</span></button></div><label class="search"><span class="sr-only">Buscar iglesia o enfoque</span><input id="search" type="search" placeholder="Buscar iglesia o enfoque…"></label></div><p id="results-status" class="results-status" aria-live="polite">12 referencias disponibles</p><div class="jump-links" aria-label="Accesos a fichas">{jump}</div><div id="cases">{cards}</div><p class="empty" hidden>No hay referencias que coincidan. Probá otro filtro o búsqueda.</p></section><section class="conclusion wrap" id="para-caudal"><p class="eyebrow">Nuestra lectura para el proyecto</p><h2>Una web que recibe.<br><em>Una comunidad que sigue.</em></h2><div class="takeaway-grid"><div><span>Bienvenida</span><p>Información de primera visita y acciones comprensibles desde el inicio.</p><small>Life.Church + Saddleback</small></div><div><span>Identidad</span><p>Fotografía real y una expresión editorial coherente con la vida de Caudal.</p><small>Bethel + Passion City</small></div><div><span>Continuidad</span><p>Mensajes, series y canales existentes que alimentan la semana.</p><small>Elevation + Missio + Rincón</small></div><div><span>Crecimiento</span><p>Una base capaz de vincular iglesia, formación e Instituto Cultura.</p><small>Hillsong + Bethel</small></div></div><div class="conclusion-action"><p>La decisión se toma por lo que representa a Caudal y por la capacidad de mantenerlo vivo.</p><a class="primary" href="../prototipos/index.html">Comparar nuestras seis propuestas ↗</a></div></section><section class="methodology wrap"><details><summary>Fuentes, fecha y límites de la revisión</summary><div><p>Consulta: {DATE}, zona de Buenos Aires. Capturas de escritorio a 1440 × 1000 y móvil a 390 × 844, en un navegador temporal sin sesión personal. El recorrido ampliado se limita a 11.000 px de alto; puede no incluir el final de portadas más extensas. Animaciones, videos, idioma, campañas y avisos pueden variar entre visitas.</p><p>Las fichas describen la portada y los enlaces visibles. No prueban el funcionamiento integral de formularios, cuentas o donaciones. Los estilos tipográficos son los declarados en CSS; no se certifica la fuente efectivamente renderizada en cada texto.</p><p>Las cifras de YouTube se consultaron en los canales institucionales enlazados por las propias webs. Son lecturas públicas redondeadas y fechadas; no se suman ministerios, música ni sedes. No se dispone de analítica privada de tráfico, alcance único, engagement o conversiones. Por eso no se asignan esas métricas ni un puesto en un ranking.</p><p>Se corrigieron las direcciones de Missio y El Rey Jesús. Se incorporó el sitio de Centro de Adoración · Ministerio Altares, Villa Sarmiento, con su correspondencia pendiente de confirmar. La referencia bautista fue confirmada por el cliente como iebcordoba.es, de Córdoba, España, y se clasifica entre las internacionales. Iglesia Adoración de Buenos Aires sigue sin identificación fiable: adoracion.co pertenece a Barranquilla, Colombia. No se acredita que todos los casos tengan más de 5.000 asistentes. Las capturas pertenecen a sus respectivos sitios y se incluyen como referencia para esta presentación.</p></div></details></section></main><footer class="footer wrap"><span>Caudal de Vida · Dossier de referentes digitales</span><span>Preparado por Diego · Octubre 2026</span><a href="../prototipos/index.html">Propuestas de diseño ↗</a></footer><aside class="selection-tray" hidden aria-label="Referentes seleccionados"><span><b class="selection-count">0</b> referentes seleccionados</span><button id="compare-open">Comparar selección ↗</button><button id="clear-selection">Limpiar</button></aside><dialog id="image-dialog" class="image-dialog" aria-labelledby="image-title"><div class="dialog-bar"><h2 id="image-title">Captura del referente</h2><button data-close>Cerrar ✕</button></div><div class="image-scroll"><img id="expanded-image" src="" alt=""></div></dialog><dialog id="compare-dialog" class="compare-dialog" aria-labelledby="compare-title"><div class="dialog-bar"><h2 id="compare-title">Referentes para conversar</h2><button data-close>Cerrar ✕</button></div><div id="comparison-content"></div><p class="compare-footnote">La selección se guarda solo en este navegador. No implica una recomendación automática ni una evaluación de resultados.</p></dialog><p class="sr-only" id="selection-status" aria-live="polite"></p></body></html>'''
    (ROOT/'index.html').write_text(html)
    print(f'Dossier generado: 12 fichas, {count} sitios capturados y {12-count} pendientes.')

if __name__ == '__main__': main()
