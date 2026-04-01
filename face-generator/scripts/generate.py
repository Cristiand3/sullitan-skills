#!/usr/bin/env python3
"""
FACE-GENERATOR: Generate custom AI faces with granular facial feature control.

Usage:
    uv run generate.py --brief "description" --output-dir <dir> [--sex female] [--ethnicity latina] ...
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

COMFY_DEPLOY_API_URL = "https://api.comfydeploy.com/api"
DEPLOYMENT_ID = "ac477523-f9d0-4e03-92e6-96bec59550f4"

FACE_PARAMS = [
    "sex", "ethnicity",
    "eye_shape", "eye_size", "eye_tilt", "eye_color",
    "eyebrow_thickness", "eyebrow_shape", "eyebrow_color",
    "nose_profile", "nose_base", "nose_tip",
    "lips_volume", "cupid_bow", "lips_proportion", "lips_color",
    "forehead", "cheekbones", "jawline", "chin", "cheeks",
    "submental", "face_neck_transition",
    "hair_structure", "hair_length", "hair_volume", "hair_color",
    "skin_tone", "skin_undertone", "skin_texture", "skin_micro_texture",
    "skin_imperfections", "skin_reflection",
    "wrinkles", "scars", "deformations", "tone_loss", "skin_marks",
    "vitiligo", "under_eye",
    "expression", "expression_variant",
]


def get_api_key():
    api_key = os.environ.get("COMFY_DEPLOY_API_KEY")
    if not api_key:
        raise ValueError("COMFY_DEPLOY_API_KEY environment variable is required")
    return api_key


def queue_generation(api_key, brief, params):
    inputs = {"brief_text": brief}
    for p in FACE_PARAMS:
        inputs[p] = params.get(p, "auto")

    payload = {
        "deployment_id": DEPLOYMENT_ID,
        "inputs": inputs,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print(f"Queuing face generation...")
    print(f"  Brief: {brief[:80]}...")
    for k, v in params.items():
        if v != "auto":
            print(f"  {k}: {v}")

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
    if not outputs:
        print("No outputs found!")
        return []

    downloaded = []
    for i, output in enumerate(outputs):
        if isinstance(output, dict):
            url = output.get("url") or output.get("data", {}).get("images", [{}])[0].get("url", "")
            filename = output.get("filename", f"face_{i+1}.png")
        elif isinstance(output, str):
            url = output
            filename = f"face_{i+1}.png"
        else:
            continue

        if not url:
            continue

        print(f"Downloading: {filename}")
        resp = requests.get(url)
        resp.raise_for_status()
        filepath = output_dir / filename
        filepath.write_bytes(resp.content)
        downloaded.append(str(filepath))

    return downloaded


def main():
    parser = argparse.ArgumentParser(description="Generate custom AI faces")
    parser.add_argument("--brief", required=True, help="Face description")
    parser.add_argument("--output-dir", required=True, help="Output directory")

    for p in FACE_PARAMS:
        arg_name = f"--{p.replace('_', '-')}"
        parser.add_argument(arg_name, default="auto", help=f"{p} (default: auto)")

    args = parser.parse_args()

    api_key = get_api_key()
    params = {}
    for p in FACE_PARAMS:
        val = getattr(args, p, "auto")
        if val != "auto":
            params[p] = val

    run_id = queue_generation(api_key, args.brief, params)
    result = poll_status(api_key, run_id)
    downloaded = download_outputs(result, args.output_dir)

    print(f"\n✅ Generated {len(downloaded)} face(s) in: {args.output_dir}")
    for f in downloaded:
        print(f"  - {Path(f).name}")


if __name__ == "__main__":
    main()
