# Proceso mensual — "Soluciones / Servicios de IA" (index.html#soluciones y servicios.html)

Fuente de verdad de edición: `/workspace/gapatic-ia`. Se sincroniza a `/workspace/GAPATIC-git` (repo `juancarlosgamboabuendia/GAPATIC`, rama `main`). No copiar nada al PC del usuario.

## Frecuencia
Primera semana de cada mes (o antes si hay un lanzamiento grande de un proveedor).

## Reglas fijas
- Español, voz GAPATIC, para empresas peruanas. 6–8 tarjetas: qué hace GAPATIC, con qué tipo de herramientas, resultado de negocio **cualitativo**.
- Solo nombrar productos/funciones confirmados abriendo la fuente oficial (WebSearch + WebFetch/curl). Nada de precios, cifras o capacidades no verificadas.
- Proveedores = "referentes tecnológicos"; nunca afirmar alianzas oficiales.
- NUNCA poner dirección física (Calle Durero 490 / San Borja).
- No tocar Insights (`#insights`, `noticias/`) ni Oportunidades (`#casos`, `casos/`).
- Mantener el diseño: `ol.specs > li > a.spec` (`spec-num`, `h3`, `p`, `spec-tag`, `more-link`). En `index.html` cada tarjeta enlaza a `servicios.html#<id>`; en `servicios.html` cada `<li>` lleva ese `id`. Si cambia un id, actualizar ambos.

## Pasos
0. **Leer el monitor de IA del usuario (antes de investigar).** Si existe `/workspace/shared/monitor-ia/`, leer todos los `.md` que haya allí (hallazgos recientes resumidos). Tratarlos solo como **pistas**: ningún producto, función o fecha entra en la web sin verificarlo en la fuente oficial (paso 1). Si la carpeta no existe o está vacía, seguir con el paso 1.
1. **Investigar novedades del mes** en fuentes oficiales: Anthropic (claude.com/blog, platform.claude.com/docs — Managed Agents, Agent SDK, Claude Code), OpenAI (openai.com/index, developers.openai.com — Agents SDK, Agents API, Codex), Google Cloud (Gemini Enterprise Agent Platform release notes, ADK), Microsoft (Copilot Studio "What's new", Learn), GitHub (Copilot cloud agent docs/changelog), Cursor (cursor.com/docs, changelog), xAI (docs.x.ai), Meta (Llama), Nous Research (Hugging Face / Hermes), MCP (modelcontextprotocol.io). Anotar URL + fecha. Revisar también productos **retirados o renombrados** (p. ej. Vertex AI → Gemini Enterprise Agent Platform; OpenAI Agent Builder deja de estar disponible el 30-nov-2026).
2. **Actualizar tarjetas y secciones** en `index.html` (sección `#soluciones`), `servicios.html` (tarjetas en `#servicios-ia-2026`, que enlazan a `#<id>`, y una sección detallada `<section id="<id>" class="service-block">` por servicio: qué hace GAPATIC, casos típicos en Perú, entregables, referentes y CTA `contacto.html?servicio=<id>`). Conservar los anclajes antiguos `consultoria-ia`, `desarrollo-ia`, `datos-ia` (spans vacíos dentro de la sección más cercana): añadir/quitar referentes, ajustar descripciones, reemplazar categorías obsoletas. Mantener ambas listas coherentes.
3. **Actualizar la línea** `Actualizado: <mes> <año>` (`p.spec-updated`) en ambas páginas.
4. **Verificar:**
   - `grep -rn "Durero\|San Borja" index.html servicios.html` → sin resultados.
   - `python3 casos/rebuild.py` → `OK` (no debe cambiar Oportunidades).
   - `python3 -m http.server 8765` y `/usr/bin/google-chrome --headless --no-sandbox --disable-gpu --window-size=1280,2600 --screenshot=/tmp/s.png http://localhost:8765/index.html` (y `servicios.html`); revisar las imágenes.
5. **Sincronizar** gapatic-ia → GAPATIC-git:
   `cd /workspace/gapatic-ia && tar --exclude=.git --exclude=_orig --exclude=original-pages.zip -cf - . | tar -xf - -C /workspace/GAPATIC-git`
   y comprobar `diff -rq --exclude=.git --exclude=_orig --exclude=original-pages.zip /workspace/gapatic-ia /workspace/GAPATIC-git` (sin salida).
6. **Publicar:** `cd /workspace/GAPATIC-git && git add -A && git commit -m "Soluciones: actualización <mes> <año>" && git push origin main`.
7. **Reportar:** hash, lista de tarjetas, fuentes verificadas, cambios de nombre/retiros detectados.

## Fuentes verificadas (octubre 2026)
- https://platform.claude.com/docs/en/managed-agents/overview · https://claude.com/blog/claude-managed-agents · https://code.claude.com/docs/en/agent-sdk/overview
- https://openai.github.io/openai-agents-python/ · https://openai.com/index/introducing-the-agents-api/ · https://openai.com/index/introducing-agentkit/ (aviso de retiro)
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview · https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use · https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent · https://cursor.com/docs/cloud-agent
- https://docs.x.ai/developers/models/grok-voice-3.0 · https://huggingface.co/NousResearch/Hermes-4-70B · https://groq.com/blog/the-official-llama-api-accelerated-by-groq
- https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
