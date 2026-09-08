#!/usr/bin/env python3
"""chroma_key.py — Cross-platform chroma-key: recover true alpha from a green-screen image.

Works on Windows, macOS, and Linux. Only requires Pillow (pip install Pillow).
Replaces the bash/ffmpeg/imagemagick pipeline with a pure-Python implementation
that gives agents a single, reliable keying tool regardless of OS.

Usage:
    python chroma_key.py input.png output.png [options]

    --key-color     Hex color to key out (default: #00FF00)
    --similarity    How close a pixel must be to key color to be removed, 0-1 (default: 0.22)
    --blend         Edge softness, 0-1 (default: 0.08)
    --despill       Remove green fringe from edges (default: on)
    --no-despill    Skip despill pass
    --trim          Trim to bounding box (default: on)
    --no-trim       Skip bounding-box trim
    --fallback      Use white/black matte difference technique instead of chroma key.
                    Expects two inputs: --white-input and --black-input
    --white-input   Path to image rendered on pure white background
    --black-input   Path to image rendered on pure black background
"""

import argparse
import math
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    if hex_color.lower().startswith("0x"):
        hex_color = hex_color[2:]
    if len(hex_color) == 6:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    raise ValueError(f"Invalid hex color: {hex_color}")


def color_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
    """Euclidean distance between two RGB colors, normalized to 0-1."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2))) / (255.0 * math.sqrt(3))


def chroma_key(
    img: Image.Image,
    key_color: tuple[int, int, int] = (0, 255, 0),
    similarity: float = 0.22,
    blend: float = 0.08,
) -> Image.Image:
    """Remove a solid background color and produce a real alpha channel.

    For each pixel, compute the normalized color distance to the key color.
    - If distance < similarity: fully transparent
    - If distance < similarity + blend: partial transparency (soft edge)
    - Otherwise: fully opaque
    """
    img = img.convert("RGBA")
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            dist = color_distance((r, g, b), key_color)

            if dist < similarity:
                # Fully transparent — this is the key color
                pixels[x, y] = (r, g, b, 0)
            elif dist < similarity + blend:
                # Partial transparency for soft edges
                alpha = int(255 * ((dist - similarity) / blend))
                pixels[x, y] = (r, g, b, alpha)
            # else: fully opaque, keep as is

    return img


def despill_green(img: Image.Image, strength: float = 0.5) -> Image.Image:
    """Remove green spill from edge pixels.

    Where green dominates red and blue, pull green toward the average of
    red and blue. This prevents keyed edges from retaining a green fringe.
    """
    img = img.convert("RGBA")
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue  # Skip fully transparent pixels

            avg_rb = (r + b) / 2
            if g > avg_rb:
                # Green dominates — pull it down
                new_g = int(g - (g - avg_rb) * strength)
                pixels[x, y] = (r, new_g, b, a)

    return img


def trim_to_bbox(img: Image.Image) -> Image.Image:
    """Trim transparent border, crop to bounding box of non-transparent pixels."""
    bbox = img.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def difference_matte(white_img: Image.Image, black_img: Image.Image) -> Image.Image:
    """Derive alpha from white-on-white and white-on-black renders.

    This is the fallback when the model can't hold a clean flat green.
    Generate the same subject once on pure white and once on pure black,
    then derive alpha from the luminance difference.

    Alpha = 1 - (white_luminance - black_luminance)
    RGB = black_rgb / alpha (where alpha > 0)
    """
    white_img = white_img.convert("RGB")
    black_img = black_img.convert("RGB")

    if white_img.size != black_img.size:
        raise ValueError(
            f"White and black images must be the same size. "
            f"Got {white_img.size} and {black_img.size}"
        )

    width, height = white_img.size
    result = Image.new("RGBA", (width, height))
    w_pixels = white_img.load()
    b_pixels = black_img.load()
    r_pixels = result.load()

    for y in range(height):
        for x in range(width):
            wr, wg, wb = w_pixels[x, y]
            br, bg, bb = b_pixels[x, y]

            # Alpha derived from the difference in luminance
            # On white bg: pixel = fg * a + 255 * (1 - a)
            # On black bg: pixel = fg * a
            # Difference: white - black = 255 * (1 - a)
            # Therefore: a = 1 - (white - black) / 255

            dr = wr - br
            dg = wg - bg
            db = wb - bb

            # Use max channel difference for most accurate alpha
            diff = max(dr, dg, db)
            alpha = 255 - diff

            if alpha <= 2:
                r_pixels[x, y] = (0, 0, 0, 0)
            elif alpha >= 253:
                r_pixels[x, y] = (br, bg, bb, 255)
            else:
                # Recover the true foreground color: fg = black_pixel / alpha
                a_norm = alpha / 255.0
                fr = min(255, int(br / a_norm))
                fg = min(255, int(bg / a_norm))
                fb = min(255, int(bb / a_norm))
                r_pixels[x, y] = (fr, fg, fb, alpha)

    return result


def verify_alpha(img: Image.Image) -> tuple[int, int]:
    """Return (min_alpha, max_alpha) across all pixels."""
    alpha = img.getchannel("A")
    return alpha.getextrema()


def main():
    parser = argparse.ArgumentParser(
        description="Recover true alpha-channel PNG from a green-screen or matte image.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", nargs="?", help="Input PNG (green-screen image)")
    parser.add_argument("output", nargs="?", help="Output PNG (with real alpha)")
    parser.add_argument(
        "--key-color",
        default="#00FF00",
        help="Background color to key out (default: #00FF00)",
    )
    parser.add_argument(
        "--similarity",
        type=float,
        default=0.22,
        help="Color distance threshold 0-1 (default: 0.22). Raise if fringing remains.",
    )
    parser.add_argument(
        "--blend",
        type=float,
        default=0.08,
        help="Edge softness 0-1 (default: 0.08)",
    )
    parser.add_argument(
        "--despill",
        action="store_true",
        default=True,
        dest="despill",
        help="Remove green spill from edges (default: on)",
    )
    parser.add_argument(
        "--no-despill",
        action="store_false",
        dest="despill",
        help="Skip the despill pass",
    )
    parser.add_argument(
        "--trim",
        action="store_true",
        default=True,
        dest="trim",
        help="Trim to bounding box (default: on)",
    )
    parser.add_argument(
        "--no-trim",
        action="store_false",
        dest="trim",
        help="Skip bounding-box trim",
    )
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="Use white/black difference matte instead of chroma key",
    )
    parser.add_argument(
        "--white-input",
        help="White-background render (for --fallback mode)",
    )
    parser.add_argument(
        "--black-input",
        help="Black-background render (for --fallback mode)",
    )

    args = parser.parse_args()

    if args.fallback:
        # Difference matte mode
        if not args.white_input or not args.black_input or not args.output:
            parser.error("--fallback requires --white-input, --black-input, and output path")

        print(f"[1/3] Loading white-bg and black-bg renders...")
        white_img = Image.open(args.white_input)
        black_img = Image.open(args.black_input)

        print(f"[2/3] Computing difference matte...")
        result = difference_matte(white_img, black_img)

        if args.trim:
            print(f"[3/3] Trimming to bounding box...")
            result = trim_to_bbox(result)
        else:
            print(f"[3/3] Skipping trim.")

    else:
        # Chroma key mode
        if not args.input or not args.output:
            parser.error("Chroma key mode requires input and output paths")

        key_rgb = hex_to_rgb(args.key_color)

        print(f"[1/4] Loading {args.input}...")
        img = Image.open(args.input)

        print(f"[2/4] Keying out {args.key_color} (similarity={args.similarity}, blend={args.blend})...")
        result = chroma_key(img, key_rgb, args.similarity, args.blend)

        if args.despill:
            print(f"[3/4] Removing green spill from edge pixels...")
            result = despill_green(result)
        else:
            print(f"[3/4] Skipping despill.")

        if args.trim:
            print(f"[4/4] Trimming to bounding box...")
            result = trim_to_bbox(result)
        else:
            print(f"[4/4] Skipping trim.")

    # Save result
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(str(output_path), "PNG")

    # Verify alpha channel
    min_a, max_a = verify_alpha(result)
    print(f"Alpha channel range: min={min_a} max={max_a}")

    if min_a == 255 and max_a == 255:
        print(
            "WARNING: No transparent pixels found — keying likely failed.",
            file=sys.stderr,
        )
        print(
            "Try raising --similarity, or use --fallback with white/black renders.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Done: {args.output}")


if __name__ == "__main__":
    main()
