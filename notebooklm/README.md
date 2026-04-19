# NotebookLM Skill

Skill agéntica para Google NotebookLM vía [notebooklm-py](https://github.com/teng-lin/notebooklm-py).

Acceso programático completo: notebooks, fuentes (URL/PDF/YouTube/Drive/audio/video), chat, research agents, y generación de podcasts, videos cinematográficos, slide decks, quizzes, flashcards, infografías, mapas mentales y tablas.

## Instalación rápida

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
notebooklm skill install
```

## Uso con Claude Code

Una vez instalada, invocar con `/notebooklm` o frases como *"crea un podcast sobre X"*.

## Origen

Copia sincronizada del `SKILL.md` oficial del proyecto upstream `teng-lin/notebooklm-py` (commit `d6cef80`). Licencia MIT — ver repo original.

## Uso en Sullitan.IA

Pipeline de contenido automatizado: ingestar fuentes de cliente → generar podcast + video + slide deck + quiz desde una misma base de conocimiento.
