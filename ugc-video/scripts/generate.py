#!/usr/bin/env python3
"""
UGC-VIDEO: Generate lip-sync videos from image + script via ComfyDeploy + ElevenLabs.

Usage:
    uv run generate.py --image <path_or_url> --script "Text to speak" --output-dir <dir> [--voice-id <id>]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

COMFY_DEPLOY_API_URL = "https://api.comfydeploy.com/api"
DEPLOYMENT_ID = "14f313d4-a437-429a-9af7-72e72e8c2c2e"
DEFAULT_VOICE_ID = "PBi4M0xL4G7oVYxKgqww"


def get_api_key():
    api_key = os.environ.get("COMFY_DEPLOY_API_KEY")
    if not api_key:
        raise ValueError("COMFY_DEPLOY_API_KEY environment variable is required")
    return api_key


def upload_image(api_key, image_path):
    """Upload local image to ComfyDeploy and return URL."""
    if image_path.startswith("http"):
        return image_path

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    import mimetypes
    content_type = mimetypes.guess_type(str(path))[0] or "image/png"

    headers = {"Authorization": f"Bearer {api_key}"}
    with open(path, "rb") as f:
        files = {"file": (path.name, f, content_type)}
        resp = requests.post(f"{COMFY_DEPLOY_API_URL}/file/upload", headers=headers, files=files)
        resp.raise_for_status()
        data = resp.json()
        return data.get("file_url") or data.get("url")


def queue_generation(api_key, image_url, script, voice_id):
    payload = {
        "deployment_id": DEPLOYMENT_ID,
        "inputs": {
            "image": image_url,
            "voice_id": voice_id,
            "script": script,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print(f"Queuing UGC video generation...")
    print(f"  Script: {script[:80]}...")
    print(f"  Voice ID: {voice_id}")

    resp = requests.post(f"{COMFY_DEPLOY_API_URL}/run/deployment/queue", json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    run_id = data.get("run_id")
    print(f"Queued run: {run_id}")
    return run_id


def poll_status(api_key, run_id, timeout=600):
    headers = {"Authorization": f"Bearer {api_key}"}
    start = time.time()
    last_status = ""

    while time.time() - start < timeout:
        resp = requests.get(f"{COMFY_DEPLOY_API_URL}/run?run_id={run_id}", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status", "unknown")

        if status != last_status:
            print(f"Status: {status}...")
            last_status = status

        if status == "success":
            print("Run completed successfully!")
            return data
        elif status in ("failed", "error", "cancelled"):
            print(f"Run failed with status: {status}")
            sys.exit(1)

        time.sleep(5)

    print(f"Timeout after {timeout}s")
    sys.exit(1)


def download_outputs(data, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = data.get("outputs", [])
    downloaded = []

    for i, output in enumerate(outputs):
        if isinstance(output, dict):
            data_dict = output.get("data", {})
            
            # Check files, videos, gifs, images
            for key in ("files", "videos", "gifs", "images"):
                items = data_dict.get(key, [])
                for j, item in enumerate(items):
                    url = item.get("url", "") if isinstance(item, dict) else item
                    filename_orig = item.get("filename", "") if isinstance(item, dict) else ""
                    if not url:
                        continue
                    
                    # Determine extension and name
                    if filename_orig:
                        filename = filename_orig
                    elif ".mp4" in url:
                        filename = f"ugc_video_{j+1}.mp4"
                    elif ".mp3" in url:
                        filename = f"ugc_audio_{j+1}.mp3"
                    elif ".gif" in url:
                        filename = f"ugc_{j+1}.gif"
                    else:
                        filename = f"ugc_{j+1}.png"
                    
                    print(f"Downloading: {filename}")
                    resp = requests.get(url)
                    resp.raise_for_status()
                    filepath = output_dir / filename
                    filepath.write_bytes(resp.content)
                    downloaded.append(str(filepath))

    return downloaded


def main():
    parser = argparse.ArgumentParser(description="Generate UGC lip-sync video")
    parser.add_argument("--image", required=True, help="Image path or URL")
    parser.add_argument("--script", required=True, help="Text for the person to say")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID, help="ElevenLabs voice ID")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")

    args = parser.parse_args()
    api_key = get_api_key()

    # Upload image if local
    image_url = upload_image(api_key, args.image)
    print(f"  Image: {image_url}")

    run_id = queue_generation(api_key, image_url, args.script, args.voice_id)
    result = poll_status(api_key, run_id, args.timeout)
    downloaded = download_outputs(result, args.output_dir)

    print(f"\n✅ Generated {len(downloaded)} file(s) in: {args.output_dir}")
    for f in downloaded:
        print(f"  - {Path(f).name}")


if __name__ == "__main__":
    main()
