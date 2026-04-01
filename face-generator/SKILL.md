---
name: face-generator
description: |
  Generate custom AI faces with granular control over facial features.
  
  ✅ USE WHEN:
  - Need to create a new model/face from scratch
  - Want specific facial features (ethnicity, eye color, skin tone, etc.)
  - Creating consistent characters for campaigns
  - Need faces for Morpheus pipeline (face → model with product)
  
  ❌ DON'T USE WHEN:
  - Already have a model/face to use → go straight to Morpheus
  - Need product shots without people → use nano-banana-pro
  - Need to edit existing images → use nano-banana-pro
---

# Face Generator

Generate custom AI faces with full control over 40+ facial parameters via ComfyDeploy.

## API Details

**Endpoint:** `https://api.comfydeploy.com/api/run/deployment/queue`
**Deployment ID:** `ac477523-f9d0-4e03-92e6-96bec59550f4`
**API Key:** Same as COMFY_DEPLOY_API_KEY

## Inputs

All parameters default to `"auto"` — only specify what you want to control.

| Category | Parameters |
|----------|-----------|
| **General** | `sex`, `ethnicity`, `brief_text` |
| **Eyes** | `eye_shape`, `eye_size`, `eye_tilt`, `eye_color` |
| **Eyebrows** | `eyebrow_thickness`, `eyebrow_shape`, `eyebrow_color` |
| **Nose** | `nose_profile`, `nose_base`, `nose_tip` |
| **Lips** | `lips_volume`, `cupid_bow`, `lips_proportion`, `lips_color` |
| **Face structure** | `forehead`, `cheekbones`, `jawline`, `chin`, `cheeks`, `submental`, `face_neck_transition` |
| **Hair** | `hair_structure`, `hair_length`, `hair_volume`, `hair_color` |
| **Skin** | `skin_tone`, `skin_undertone`, `skin_texture`, `skin_micro_texture`, `skin_imperfections`, `skin_reflection` |
| **Skin details** | `wrinkles`, `scars`, `deformations`, `tone_loss`, `skin_marks`, `vitiligo`, `under_eye` |
| **Expression** | `expression`, `expression_variant` |

## Usage

```bash
uv run ~/.openclaw/workspace/skills/face-generator/scripts/generate.py \
  --brief "Young latina woman, confident smile" \
  --output-dir ./faces \
  [--sex female] \
  [--ethnicity latina] \
  [--eye-color brown] \
  [--hair-length long] \
  [--skin-tone olive]
```

## Pipeline Integration

1. **Face Generator** → create the face/model
2. **Morpheus** → put model with product in scene
3. **Multishot** → generate 10 angle variations
4. **VEED** → lip-sync video
