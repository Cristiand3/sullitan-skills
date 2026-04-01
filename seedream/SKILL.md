---
name: seedream
description: |
  Generate and edit images with SeedREAM 5.0 (ByteDance) via Replicate API.
  
  ✅ USE WHEN:
  - Need high-quality photorealistic or artistic image generation
  - Want to use photographic language (film stocks, lenses, lighting setups)
  - Need example-based editing (show before/after pair, apply to new image)
  - Need multi-step visual reasoning (sorting, classifying, transforming)
  - Want precise text rendering in images (use double quotes)
  - Need batch generation of related images (storyboards, brand packages)
  - Want to edit images using visual markers (arrows, colored regions)
  - Need domain-specific visuals (architecture renders, scientific illustrations)
  
  ❌ DON'T USE WHEN:
  - Need vector/SVG output → use recraft
  - Need product + model advertising shots → use morpheus-fashion-design
  - Need video → use sora
  - Need quick simple image gen → use nano-banana-pro
  
  REQUIRES: REPLICATE_API_TOKEN env var
---

# SeedREAM 5.0

Generate and edit images using ByteDance's SeedREAM 5.0 model via Replicate.

## Quick Start

Generate an image:
```bash
uv run {baseDir}/scripts/generate.py --prompt "A cinematic portrait, shallow depth of field, Kodak Portra 400 film look" --filename output.png
```

With input image(s) for editing:
```bash
uv run {baseDir}/scripts/generate.py --prompt "Reimagine as a watercolor painting" -i input.jpg --filename output.png
```

Example-based editing (3 images: before, after, target):
```bash
uv run {baseDir}/scripts/generate.py --prompt "Reference the change from Image 1 to Image 2, apply the same operation to Image 3" -i before.jpg -i after.jpg -i target.jpg --filename output.png
```

Batch generation:
```bash
uv run {baseDir}/scripts/generate.py --prompt "Product photo of sneakers" --batch 5 --filename output.png
```

## Options

| Flag | Description | Default |
|---|---|---|
| `--prompt, -p` | Text prompt (required) | — |
| `--image, -i` | Input image (repeat for multi-image, up to 14) | — |
| `--negative, -n` | Negative prompt | — |
| `--aspect-ratio, -a` | 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9 | 1:1 |
| `--resolution, -r` | 2K or 3K | 2K |
| `--format, -f` | png or jpg | png |
| `--filename, -o` | Output path | seedream_output.png |
| `--seed, -s` | Seed for reproducibility | — |
| `--batch, -b` | Generate N images with random seeds | — |

## Prompting Guide

**Use natural language** — describe scenes like a photographer would. The model understands film stocks (Kodak Portra, Fujifilm Velvia), lens types (50mm Summilux, anamorphic), lighting setups (golden hour backlit, chiaroscuro), and camera settings.

**For text in images** — wrap in double quotes: `A storefront sign that reads "SulliTan.ia"`

**For edits** — be specific about what to keep: "Replace the background with a beach sunset, keeping the person's pose and expression unchanged."

For detailed prompting examples and techniques, see [references/prompting-guide.md](references/prompting-guide.md).

## Key Capabilities

1. **Generación de imágenes** — fotorrealismo, arte, ilustración con calidad excepcional
2. **Edición por ejemplos** — mostrá un antes/después y aplicalo a otra imagen
3. **Razonamiento multi-paso** — clasifica, ordena, transforma con lógica
4. **Texto preciso** — renderiza texto legible dentro de imágenes
5. **Conocimiento de dominio** — arquitectura, ciencia, diseño técnico
6. **Lotes** — generá sets relacionados de imágenes
