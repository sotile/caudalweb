# Seis prototipos del inicio de Caudal de Vida

Abrir `index.html` en el navegador para comparar las propuestas. Cada una tiene una portada completa, navegación entre secciones, menú móvil, preguntas frecuentes y reproducción de mensajes en un diálogo con video visible. Los enlaces a WhatsApp, Maps y los canales oficiales son reales; no se envía nada automáticamente.

Para probar los videos con un origen HTTP y encabezados adecuados, ejecutar desde esta carpeta:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Luego visitar http://127.0.0.1:8765/. Algunos navegadores o videos pueden restringir la inserción; el diálogo siempre ofrece abrir el mensaje en YouTube.

## Las propuestas

1. Casa abierta: bienvenida cálida, fotografías rectangulares y tono editorial contemporáneo.
2. El encuentro: dirección principal, fotografía cinematográfica, azul y arena, y experiencia de reunión.
3. Vida para la Ciudad: retícula editorial y protagonismo de la misión.
4. Tu siguiente paso: señalética, recorrido y bloques de orientación.
5. Esta semana en Caudal: portada modular de contenidos, mensajes y actividades.
6. Un lugar para vos: exploración experimental con tipografía de gran escala, fotos en profundidad y tres capítulos animados con scroll nativo.

## Revisión estética y apariencias

Las seis propuestas tienen paletas clara y oscura, con un selector en la barra superior y enlaces directos desde la galería (`?theme=light` / `?theme=dark`). La elección se conserva en este navegador al cambiar de propuesta; un enlace con apariencia explícita tiene prioridad. La segunda abre inicialmente en oscuro cuando no hay una preferencia guardada.

La sexta usa una escena fija durante un tramo del scroll en escritorio, con desplazamiento, escala y transición de tres capítulos. No intercepta rueda ni gestos. En móvil y con `prefers-reduced-motion` muestra los capítulos consecutivos, sin fijación ni animaciones. Sin JavaScript el contenido también permanece visible. Los capítulos fuera de escena no reciben el foco de teclado.

## Contenido y alcance

Fotografías y miniaturas públicas de la web existente, Instagram y YouTube de Caudal. La procedencia de los archivos está en `assets/fuentes.json`. Textos basados en el documento y plan de trabajo. No se inventaron testimonios, estadísticas ni fechas de actividades.

La agenda es de muestra y no confirma convocatorias vigentes. Se indica consultar horarios porque los canales tienen diferencias. Confirmar contactos, datos, derechos de uso y contenidos antes de pasar a producción. Instituto Cultura requiere una definición de su integración y no se equipara con Cultura Jóvenes.

Son prototipos HTML locales; no hay CMS, sincronización de feeds, formularios de captura ni sitio publicado. El modo podcast queda pendiente de definir. La música se abre en la playlist oficial, sin extracción de audio. No se modificó la web existente.

## Archivos

`generar.py` genera la galería y los seis HTML. `templates/` conserva las secciones HTML compartidas y el pie. `styles.css` contiene la base y `refinements.css` la revisión estética y ambas paletas; `app.js` implementa menú, apariencia, selector, relato de scroll y diálogo de video. `theme-init.js` resuelve la apariencia antes de cargar CSS. `previews/` contiene capturas de las doce variantes para la galería.

Regenerar después de editar plantillas:

```sh
python3 generar.py
```

## Verificación realizada

Revisadas las doce variantes (seis propuestas en claro y oscuro) a 1440 × 1000, 390 × 844 y 320 × 780 en Chrome. Se comprueban cambio y persistencia de apariencia, miniaturas por modo, scroll de la sexta y alternativa con movimiento reducido. Sin desbordes horizontales, imágenes faltantes ni excepciones JavaScript. Verificados menú móvil, preguntas frecuentes y apertura/cierre del diálogo con eliminación del iframe. La prueba del diálogo no certifica la reproducción de extremo a extremo de YouTube, que depende de sus restricciones y del navegador. Se verificaron enlaces internos y existencia de archivos locales. Resultados en `verificacion.json`.
