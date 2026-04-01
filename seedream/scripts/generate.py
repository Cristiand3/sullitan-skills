#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""SeedREAM 5.0 image generation via Replicate API."""
import argparse, httpx, os, sys, time, base64
from pathlib import Path

API_URL = "https://api.replicate.com/v1/predictions"
MODEL_VERSION = "bytedance/seedream-5:eeb2857d94c49a5bcbc9d6c6057416e1d3b1a2735a16e08e4def9bf7ee22ec71"

def get_token():
    t = os.environ.get("REPLICATE_API_TOKEN")
    if not t:
        print("Set REPLICATE_API_TOKEN env var", file=sys.stderr)
        sys.exit(1)
    return t

def image_to_uri(path: str) -> str:
    if path.startswith("http"):
        return path
    p = Path(path)
    if not p.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    ext = p.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}.get(ext, "image/png")
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"

def run_single(args):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Parse model/version
    parts = MODEL_VERSION.split(":")
    version = parts[1] if len(parts) > 1 else parts[0]

    inp = {
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "output_format": args.format,
    }

    if args.image:
        inp["image_input"] = [image_to_uri(img) for img in args.image]

    body = {"version": version, "input": inp}

    with httpx.Client(timeout=300) as c:
        r = c.post(API_URL, headers=headers, json=body)
        r.raise_for_status()
        pred = r.json()
        poll_url = pred.get("urls", {}).get("get", f"{API_URL}/{pred['id']}")

        print("Generando imagen...", file=sys.stderr)
        while True:
            time.sleep(3)
            r = c.get(poll_url, headers=headers)
            r.raise_for_status()
            data = r.json()
            status = data.get("status")
            if status == "succeeded":
                break
            elif status in ("failed", "canceled"):
                print(f"Error: {data.get('error', 'Unknown')}", file=sys.stderr)
                sys.exit(1)

        output = data.get("output")
        if not output:
            print("No output", file=sys.stderr)
            sys.exit(1)

        urls = output if isinstance(output, list) else [output]
        out_path = Path(args.filename)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        for i, url in enumerate(urls):
            fname = out_path.with_stem(f"{out_path.stem}_{i+1}") if len(urls) > 1 else out_path
            fname.write_bytes(c.get(url).content)
            print(f"Image saved: {fname}")
            print(f"MEDIA:{fname}")

def main():
    p = argparse.ArgumentParser(description="SeedREAM 5.0 — generación de imágenes")
    p.add_argument("--prompt", "-p", required=True)
    p.add_argument("--image", "-i", action="append", help="Imagen(es) de entrada, repetir hasta 14x")
    p.add_argument("--aspect-ratio", "-a", default="1:1",
                   choices=["1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9"])
    p.add_argument("--resolution", "-r", default="1024", choices=["1024", "2048", "3072"],
                   help="Tamaño base en px (default: 1024)")
    p.add_argument("--format", default="png", choices=["png", "jpg"])
    p.add_argument("--filename", "-o", default="seedream_output.png")
    p.add_argument("--seed", "-s", type=int)
    p.add_argument("--batch", "-b", type=int, help="Generar N imágenes con seeds aleatorios")
    args = p.parse_args()

    if args.batch and args.batch > 1:
        import random
        base_path = Path(args.filename)
        for i in range(args.batch):
            args.seed = random.randint(0, 2**32)
            args.filename = str(base_path.with_stem(f"{base_path.stem}_{i+1}"))
            run_single(args)
    else:
        run_single(args)

if __name__ == "__main__":
    main()
