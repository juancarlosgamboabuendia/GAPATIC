# Proceso diario — "Oportunidades de IA para empresas peruanas"

Fuente de verdad de edición: `/workspace/gapatic-ia`. Se sincroniza a `/workspace/GAPATIC-git` (repo `juancarlosgamboabuendia/GAPATIC`, rama `main`) y se publica. No copiar nada al PC del usuario.

## Reglas fijas
- Español, voz GAPATIC, texto original dirigido a empresas peruanas.
- NUNCA poner dirección física (Calle Durero 490 / San Borja). `rebuild.py` falla si la encuentra.
- Toda cifra debe venir de una fuente pública que se haya **abierto de verdad** (WebFetch/curl) — INEI, BCRP, SUNAT, MIDAGRI, SBS, gob.pe, prensa seria — y citarse con enlace en el texto y en la línea "Fuente:" al final. Si no hay fuente leída, no hay números.
- `tipo: "Oportunidad"` (escenario ilustrativo) salvo que el usuario confirme un proyecto real (`"Caso real"`). Toda Oportunidad lleva el aviso visible: *"Caso aplicable: escenario ilustrativo basado en el contexto peruano, no un proyecto ejecutado para un cliente."*
- "Resultados esperados" = estimaciones/hipótesis, rotuladas como tales; nunca como logros.
- NUNCA borrar items antiguos: el catálogo se acumula (a diferencia de Insights).

## Pasos
1. **Elegir categoría, luego sector y problema.** Leer `casos/casos.json`.
   - **Categoría** (campo `categoria`, obligatorio): una de las categorías de Insights tal como aparecen en `noticias/posts.json` (hoy: Ciberseguridad, Estrategia, Gobernanza, Infraestructura, Operaciones, Productividad; si Insights añade otra, también vale). Rotar: **nunca la misma categoría que el item del día anterior**, y elegir la que tenga menos items en el catálogo (cobertura equilibrada); en empate, la usada hace más tiempo.
   - **Sector peruano** (campo `sector`, detalle secundario): agroexportación, minería, retail/bodegas, fintech, logística, salud, educación, manufactura, construcción, pesca, banca/microfinanzas, sector público, turismo, energía, telecom, seguros. Evitar repetir el sector del día anterior.
   - **Problema** (campo `problema`): uno que no exista ya en el catálogo; la combinación categoría/sector/problema debe ser nueva y coherente (p. ej. Ciberseguridad + fintech: fraude Yape/Plin).
2. **Investigar.** Buscar 1–2 fuentes públicas peruanas y abrirlas. Anotar URL, entidad y fecha.
3. **Escribir la página** `oportunidad-YYYY-MM-DD-<slug>.html` en la raíz de `/workspace/gapatic-ia`, copiando como plantilla la oportunidad más reciente (mismo `<head>`, header, footer, `article-shell`). Secciones obligatorias, en orden:
   `Contexto en Perú` · `El reto` · `Solución con IA (GAPATIC)` · `Resultados esperados (estimaciones, no resultados obtenidos)` · `Requisitos` (datos, plazo orientativo, inversión aproximada como guía) · `Criterio GAPATIC` · botón `¿Tu empresa tiene este reto? Hablemos` → `contacto.html` · línea `Fuente:`.
   Actualizar title, meta description, og:*, `article-meta` (`<span class="cat">CATEGORÍA</span>` primero, luego `<span>Sector: …</span>`, tipo, fecha "Publicado el D de mes, AAAA", servicio). Imagen: una existente en `images/`.
4. **Anteponer al JSON** (`casos/casos.json`, más reciente primero) un objeto con:
   `slug, date (America/Lima), title, home_title (corto, para la portada), categoria, sector, problema, servicio, excerpt, image, image_alt, url, tipo, fuentes[]`.
5. **Reconstruir:** `cd /workspace/gapatic-ia && python3 casos/rebuild.py` (regenera filtros por categoría y tarjetas de `proyectos.html` y las 3 más recientes en `index.html#casos`; valida campos, que `categoria` sea una categoría de Insights y aparezca en el `article-meta`, enlaces, imágenes, aviso y dirección prohibida). Debe imprimir `OK`. Correrlo dos veces no debe cambiar nada.
6. **Verificar render:** `python3 -m http.server 8765` y
   `/usr/bin/google-chrome --headless --no-sandbox --disable-gpu --window-size=1280,2200 --screenshot=/tmp/x.png http://localhost:8765/<página>` para la nueva página, `proyectos.html` e `index.html`.
7. **Sincronizar gapatic-ia → GAPATIC-git:**
   `cd /workspace/gapatic-ia && tar --exclude=.git --exclude=_orig --exclude=original-pages.zip -cf - . | tar -xf - -C /workspace/GAPATIC-git` (rsync no está instalado; no borra `.gitignore`/`README.md`). Comprobar con `diff -rq --exclude=.git --exclude=_orig --exclude=original-pages.zip /workspace/gapatic-ia /workspace/GAPATIC-git` (sin salida).
8. **Publicar:** `cd /workspace/GAPATIC-git && git add -A && git commit -m "Oportunidad diaria: <título>" && git push origin main`.
9. **Reportar:** hash, título, archivo, categoría, sector, fuentes, incidencias.
