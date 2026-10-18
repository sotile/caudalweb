# Dossier de referentes para Caudal de Vida

Abrir `index.html` en el navegador. Funciona como presentación local y se enlaza con las seis propuestas en `../prototipos/index.html`.

`Dossier referentes Caudal de Vida.pdf` es la versión de presentación exportada. El botón Imprimir / PDF permite volver a generar una versión según los filtros activos.

Incluye doce fichas: once sitios o portales capturados y una referencia sin identificación fiable (Iglesia Adoración, Buenos Aires). Se corrigieron los enlaces de El Rey Jesús y Missio. Centro de Adoración se documenta como Ministerio Altares, Villa Sarmiento; su correspondencia con la referencia genérica original queda pendiente. El cliente confirmó IEB Córdoba como https://iebcordoba.es/, de Córdoba, España: reemplaza el portal argentino provisional y pasa a referencias internacionales (siete internacionales y cinco argentinas). No se inventaron capturas ni cifras.

## Uso en reunión

- Filtrar entre Mundo y Argentina, o buscar por nombre y enfoque.
- Ampliar capturas de escritorio, móvil o del recorrido extendido.
- Seleccionar hasta tres referentes y abrir una comparación de sus aportes a Caudal. La selección queda solo en ese navegador.
- Usar Imprimir / PDF para imprimir las fichas visibles. Limpiar filtros para imprimir el dossier completo.
- Pasar a las seis propuestas propias desde la navegación superior o el cierre.

## Evidencia y alcance

Consulta: 17 de octubre de 2026, zona de Buenos Aires. Capturas de escritorio a 1440 × 1000 y móvil a 390 × 844; recorrido extendido hasta 11.000 px de alto. Se conservan los estados observados, incluidos avisos y recursos incompletos. No se usaron cuentas personales.

Las cifras de YouTube son lecturas públicas redondeadas del canal especificado y tienen fecha y enlace. No representan audiencia única, tráfico web, engagement ni tamaño de congregación. No se suman canales musicales, ministerios o sedes. Las fichas son una revisión de presentación y contenido de la portada, no una auditoría técnica ni una prueba integral de funciones internas.

## Archivos

- `capturas/`: imágenes reales de navegador.
- `datos/`: observaciones de portada, enlaces, estilos CSS declarados, comprobación de dominios y lecturas públicas de canales.
- `generar.py`: contenido editorial y generación del HTML y datos de selección.
- `capturar.cjs`: consulta de portadas mediante una instancia temporal de Chrome con DevTools en el puerto 9342 (configurable con `CDP_PORT`).
- `medir-alcance.py`: lectura puntual de canales públicos enlazados desde los sitios institucionales.
- `styles.css`, `app.js`: diseño, filtros, comparación, ampliación e impresión.

Para regenerar el dossier a partir de los datos guardados:

```sh
python3 referentes/generar.py
```

Para actualizar capturas, iniciar un Chrome temporal con `--remote-debugging-port=9342` y un directorio de perfil aislado. Ejecutar `node --experimental-websocket referentes/capturar.cjs`, revisar las capturas y actualizar las fichas antes de regenerar. Para capturar solo algunos casos, usar `CAPTURE_IDS=rey-jesus,centro-adoracion`. Los textos interpretativos no se actualizan automáticamente.

Para revisar ambos entregables mediante HTTP desde la raíz del proyecto:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Visitar http://127.0.0.1:8766/referentes/ y http://127.0.0.1:8766/prototipos/.
