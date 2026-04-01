---
name: ugc-video
description: |
  Generate UGC-style videos with AI lip-sync from a single image + script.
  
  ✅ USE WHEN:
  - Have an image of a person and want them to "speak"
  - Creating UGC promotional videos
  - Need lip-sync video from still image
  
  ❌ DON'T USE WHEN:
  - Don't have an image yet → use Morpheus or Face Generator first
  - Need multiple angles → use Multishot first, then UGC each
  - Need video without speech → use Sora
---

# UGC Video (Lip-Sync)

Generate UGC-style videos with AI lip-sync via ComfyDeploy + ElevenLabs.

## API Details

**Endpoint:** `https://api.comfydeploy.com/api/run/deployment/queue`
**Deployment ID:** `14f313d4-a437-429a-9af7-72e72e8c2c2e`
**API Key:** COMFY_DEPLOY_API_KEY
**Voice API:** ElevenLabs (ELEVENLABS_API_KEY)

## Inputs

| Input | Description |
|-------|-------------|
| `image` | URL of the person image |
| `voice_id` | ElevenLabs voice ID |
| `script` | Text the person will say (dialogue only) |

## Pipeline

1. **Face Generator** or **Morpheus** → create person image
2. **Multishot** → 10 angle variations (optional)
3. **UGC Video** → lip-sync video for each selected shot
4. **ffmpeg/Remotion** → edit final video

## Voice IDs

Cristian selects voice per job. Default generic: `PBi4M0xL4G7oVYxKgqww`

To list available voices:
```bash
curl -s -H "xi-api-key: $ELEVENLABS_API_KEY" https://api.elevenlabs.io/v1/voices | python3 -m json.tool
```
