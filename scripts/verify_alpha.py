#!/usr/bin/env python3
"""verify_alpha.py — Verify that PNG images have real transparent pixels.

Run this before compositing any asset into the scene. An asset that claims
to be transparent but has alpha=255 everywhere will composite as a solid
rectangle and break the layered scene.

Usage:
    # Single file
    python verify_alpha.py asset.png

    # Batch: all PNGs in a directory
    python verify_alpha.py assets/

    # Strict mode: fail if any fully-opaque or fully-transparent asset
    python verify_alpha.py --strict assets/

    # Show histogram of alpha values
    python verify_alpha.py --histogram asset.png
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def analyze_alpha(image_path: Path) -> dict:
    """Analyze the alpha channel of a PNG image.

    Returns a dict with:
        - path: file path
        - has_alpha: whether the image has an alpha channel at all
        - min_alpha: minimum alpha value (0-255)
        - max_alpha: maximum alpha value (0-255)
        - fully_opaque: True if every pixel is alpha=255
        - fully_transparent: True if every pixel is alpha=0
        - transparent_pixel_pct: percentage of fully transparent pixels
        - opaque_pixel_pct: percentage of fully opaque pixels
        - partial_pixel_pct: percentage of partially transparent pixels
        - verdict: PASS, WARN, or FAIL
    """
    img = Image.open(image_path)

    if img.mode != "RGBA":
        return {
            "path": str(image_path),
            "has_alpha": False,
            "verdict": "FAIL",
            "reason": f"Image mode is {img.mode}, not RGBA — no alpha channel exists",
        }

    alpha = img.getchannel("A")
    min_a, max_a = alpha.getextrema()
    total_pixels = img.size[0] * img.size[1]

    # Count pixel types
    alpha_data = list(alpha.getdata())
    transparent = sum(1 for a in alpha_data if a == 0)
    opaque = sum(1 for a in alpha_data if a == 255)
    partial = total_pixels - transparent - opaque

    result = {
        "path": str(image_path),
        "has_alpha": True,
        "min_alpha": min_a,
        "max_alpha": max_a,
        "fully_opaque": min_a == 255,
        "fully_transparent": max_a == 0,
        "transparent_pixel_pct": round(transparent / total_pixels * 100, 1),
        "opaque_pixel_pct": round(opaque / total_pixels * 100, 1),
        "partial_pixel_pct": round(partial / total_pixels * 100, 1),
        "total_pixels": total_pixels,
    }

    if min_a == 255 and max_a == 255:
        result["verdict"] = "FAIL"
        result["reason"] = "Every pixel is fully opaque — no transparency exists. Keying likely failed."
    elif max_a == 0:
        result["verdict"] = "FAIL"
        result["reason"] = "Every pixel is fully transparent — the entire image is empty."
    elif transparent / total_pixels < 0.01:
        result["verdict"] = "WARN"
        result["reason"] = (
            f"Only {result['transparent_pixel_pct']}% transparent pixels. "
            f"The background may not have been fully removed."
        )
    else:
        result["verdict"] = "PASS"
        result["reason"] = (
            f"{result['transparent_pixel_pct']}% transparent, "
            f"{result['opaque_pixel_pct']}% opaque, "
            f"{result['partial_pixel_pct']}% partial."
        )

    return result


def print_histogram(image_path: Path):
    """Print a simple text histogram of alpha values."""
    img = Image.open(image_path).convert("RGBA")
    alpha = img.getchannel("A")
    alpha_data = list(alpha.getdata())

    # Bucket into 16 bins
    bins = [0] * 16
    for a in alpha_data:
        bucket = min(a // 16, 15)
        bins[bucket] += 1

    total = len(alpha_data)
    max_count = max(bins)

    print(f"\nAlpha histogram for {image_path.name}:")
    print(f"{'Range':>10}  {'Count':>8}  {'Pct':>6}  Bar")
    print("-" * 60)

    for i, count in enumerate(bins):
        lo = i * 16
        hi = min((i + 1) * 16 - 1, 255)
        pct = count / total * 100
        bar_len = int(count / max_count * 30) if max_count > 0 else 0
        bar = "█" * bar_len
        print(f"{lo:>3}-{hi:<3}     {count:>8}  {pct:>5.1f}%  {bar}")


def main():
    parser = argparse.ArgumentParser(
        description="Verify that PNG images have real transparent pixels.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="PNG file(s) or directory(ies) to verify",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 on any WARN or FAIL (default: only FAIL)",
    )
    parser.add_argument(
        "--histogram",
        action="store_true",
        help="Show alpha value histogram for each file",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print failures and warnings",
    )

    args = parser.parse_args()

    # Collect all PNG files
    png_files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            png_files.extend(sorted(path.glob("**/*.png")))
        elif path.is_file() and path.suffix.lower() == ".png":
            png_files.append(path)
        else:
            print(f"Skipping non-PNG: {path}", file=sys.stderr)

    if not png_files:
        print("No PNG files found.", file=sys.stderr)
        sys.exit(1)

    # Analyze each file
    results = []
    has_failure = False
    has_warning = False

    for png_path in png_files:
        result = analyze_alpha(png_path)
        results.append(result)

        icon = {"PASS": "✓", "WARN": "⚠", "FAIL": "✗"}.get(result["verdict"], "?")

        if result["verdict"] == "FAIL":
            has_failure = True
            print(f"  {icon} FAIL  {png_path.name}: {result['reason']}")
        elif result["verdict"] == "WARN":
            has_warning = True
            print(f"  {icon} WARN  {png_path.name}: {result['reason']}")
        elif not args.quiet:
            print(f"  {icon} PASS  {png_path.name}: {result['reason']}")

        if args.histogram:
            print_histogram(png_path)

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["verdict"] == "PASS")
    warned = sum(1 for r in results if r["verdict"] == "WARN")
    failed = sum(1 for r in results if r["verdict"] == "FAIL")

    print(f"\n{'─' * 40}")
    print(f"Verified {total} file(s): {passed} passed, {warned} warned, {failed} failed")

    if has_failure:
        print("\nACTION REQUIRED: Re-run chroma_key.py with adjusted parameters on failed assets.")
        sys.exit(1)
    elif has_warning and args.strict:
        print("\nACTION REQUIRED (strict mode): Investigate warned assets.")
        sys.exit(1)
    else:
        print("\nAll assets verified — safe to composite.")


if __name__ == "__main__":
    main()
