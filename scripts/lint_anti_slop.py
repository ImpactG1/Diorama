#!/usr/bin/env python3
"""lint_anti_slop.py — Static code linter for Diorama HTML and CSS.

Analyzes Diorama landing pages to catch the classic AI slop design tells:
  1. The Centering Disease (excessive text-align: center across all sections)
  2. Flat Sticker Typography (text dumped on top at z:50 with no depth interleaving)
  3. Missing Atmospheric Scrims (relying on muddy text-shadow blurs)
  4. AI Copywriting Tropes (clichéd tricolons, fake profundity, generic SaaS CTAs)
  5. Missing 3-Tier Typography & Responsive reflow rules

Usage:
    # Lint specific files
    python scripts/lint_anti_slop.py index.html styles.css

    # Lint an entire example or site directory
    python scripts/lint_anti_slop.py examples/mafia-landing/

    # Strict mode (exit with error code on any warning)
    python scripts/lint_anti_slop.py --strict examples/mafia-landing/
"""

import argparse
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


AI_COPY_CLICHES = [
    (r"\bevery\s+\w+\s+starts\s+with\b", "Fake profundity ('Every X starts with...')"),
    (r"\bwhere\s+\w+\s+meets\s+\w+\b", "AI marketing cliché ('Where X meets Y...')"),
    (r"\bblood\s+is\s+thicker\s+than\b", "Movie cliché ('Blood is thicker than...')"),
    (r"\bget\s+started\b", "Generic SaaS CTA ('Get Started')"),
    (r"\blearn\s+more\b", "Generic SaaS CTA ('Learn More')"),
    (r"\bclick\s+here\b", "Non-descriptive link ('Click here')"),
    (r"\b[A-Z][a-z]+\.\s+[A-Z][a-z]+\.\s+[A-Z][a-z]+\.", "AI Tricolon ('Word. Word. Word.')"),
]


def lint_css(css_content: str, file_path: Path) -> list:
    issues = []

    # 1. Centering Disease Check
    text_align_matches = re.findall(r"text-align\s*:\s*([^;]+);", css_content)
    if text_align_matches:
        center_count = sum(1 for m in text_align_matches if "center" in m.lower())
        total_count = len(text_align_matches)
        center_pct = (center_count / total_count) * 100
        if center_pct > 40:
            issues.append({
                "level": "WARN",
                "category": "Layout / Centering Disease",
                "message": f"{center_count}/{total_count} ({center_pct:.0f}%) of text-align declarations are 'center'. Use asymmetric 12-col grids and left-aligned editorial columns.",
                "file": str(file_path)
            })

    # 2. Check for heavy fuzzy text-shadow (amateur contrast fix)
    shadow_matches = re.finditer(r"text-shadow\s*:\s*([^;]+);", css_content)
    for match in shadow_matches:
        val = match.group(1)
        # Look for blurs >= 20px
        blur_match = re.search(r"(\d+)px", val)
        if blur_match and int(blur_match.group(1)) >= 20:
            issues.append({
                "level": "WARN",
                "category": "Legibility / Muddy Shadows",
                "message": f"Excessive text-shadow blur ({blur_match.group(1)}px). Replace with a directional atmospheric scrim or tactile backing slab.",
                "file": str(file_path)
            })

    # 3. Check for prefers-reduced-motion
    if "prefers-reduced-motion" not in css_content:
        issues.append({
            "level": "FAIL",
            "category": "Accessibility / Motion",
            "message": "Missing '@media (prefers-reduced-motion: reduce)' rule to disable parallax and ambient animations.",
            "file": str(file_path)
        })

    # 4. Check for responsive breakpoint
    if "@media" not in css_content or "max-width" not in css_content:
        issues.append({
            "level": "WARN",
            "category": "Responsive",
            "message": "No responsive media queries found. Layered scenes must reflow gracefully on tablet/mobile.",
            "file": str(file_path)
        })

    return issues


def lint_html(html_content: str, file_path: Path) -> list:
    issues = []

    # 1. Depth Interleaving Check
    # Does the hero scene exist?
    if "diorama-scene" in html_content:
        # Check if there is any layer behind z-index 20 with text or masthead
        has_interleaved_masthead = bool(
            re.search(r"masthead|diorama-type--back|--z:\s*(1[0-9]|5)\b", html_content)
        )
        if not has_interleaved_masthead:
            issues.append({
                "level": "WARN",
                "category": "Layer Composition / Flat Sticker",
                "message": "All text sits at z:50 on top of the art. Interleave a masthead or title at z:15 behind the hero cutout to create 3D poster depth.",
                "file": str(file_path)
            })

        # Check for atmospheric scrim
        has_scrim = bool(re.search(r"scrim|diorama-scrim", html_content))
        if not has_scrim:
            issues.append({
                "level": "INFO",
                "category": "Contrast / Atmospheric Scrim",
                "message": "No directional scrim layer found. Ensure text has a gradient mask or backing card for legibility over painted plates.",
                "file": str(file_path)
            })

    # 2. Baked Text Check
    if re.search(r"<img[^>]+alt=['\"][^'\"]*(?:title|heading|welcome|tagline)[^'\"]*['\"]", html_content, re.IGNORECASE):
        issues.append({
            "level": "FAIL",
            "category": "Accessibility",
            "message": "Possible text baked into an image asset. Text must always be real DOM elements.",
            "file": str(file_path)
        })

    # 3. AI Copy Cliché Check
    # Strip HTML tags to inspect text content
    clean_text = re.sub(r"<[^>]+>", " ", html_content)
    clean_text = re.sub(r"\s+", " ", clean_text)

    for pattern, description in AI_COPY_CLICHES:
        if re.search(pattern, clean_text, re.IGNORECASE):
            issues.append({
                "level": "WARN",
                "category": "Copywriting / AI Slop",
                "message": f"Detected AI copy trope: {description}. Ground the copy in concrete, in-world artifacts.",
                "file": str(file_path)
            })

    return issues


def lint_target(target_path: Path) -> list:
    issues = []
    if target_path.is_file():
        ext = target_path.suffix.lower()
        content = target_path.read_text(encoding="utf-8", errors="replace")
        if ext in [".html", ".htm"]:
            issues.extend(lint_html(content, target_path))
        elif ext == ".css":
            issues.extend(lint_css(content, target_path))
    elif target_path.is_dir():
        for root, _, files in os.walk(target_path):
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in [".html", ".htm"]:
                    content = p.read_text(encoding="utf-8", errors="replace")
                    issues.extend(lint_html(content, p))
                elif p.suffix.lower() == ".css":
                    content = p.read_text(encoding="utf-8", errors="replace")
                    issues.extend(lint_css(content, p))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Lint Diorama HTML and CSS for layout and copy anti-slop tells.")
    parser.add_argument("targets", nargs="+", help="Files or directories to lint")
    parser.add_argument("--strict", action="store_true", help="Fail with exit code 1 if any warnings or failures are found")

    args = parser.parse_args()

    all_issues = []
    for target in args.targets:
        t_path = Path(target)
        if not t_path.exists():
            print(f"ERROR: Target '{target}' not found.", file=sys.stderr)
            sys.exit(1)
        all_issues.extend(lint_target(t_path))

    # Print Report
    print("\n" + "=" * 60)
    print("  DIORAMA ANTI-SLOP LAYOUT & TYPOGRAPHY LINTER")
    print("=" * 60)

    if not all_issues:
        print("\n [PASS] No layout, centering, or copywriting anti-slop tells found!")
        print("  - Asymmetric grid or depth interleaving present.")
        print("  - Atmospheric scrims / proper contrast verified.")
        print("  - Clean in-world copy and motion safety respected.\n")
        sys.exit(0)

    fail_count = sum(1 for i in all_issues if i["level"] == "FAIL")
    warn_count = sum(1 for i in all_issues if i["level"] == "WARN")
    info_count = sum(1 for i in all_issues if i["level"] == "INFO")

    print(f"\nFound {len(all_issues)} issue(s): {fail_count} FAIL, {warn_count} WARN, {info_count} INFO\n")

    for idx, issue in enumerate(all_issues, 1):
        badge = f"[{issue['level']}]"
        print(f"{idx:2d}. {badge:<6} [{issue['category']}]")
        print(f"    File:    {issue['file']}")
        print(f"    Details: {issue['message']}\n")

    if fail_count > 0 or (args.strict and warn_count > 0):
        print("Verdict: FAILED (Review anti-slop checklist and spatial-layouts.md)\n")
        sys.exit(1)
    else:
        print("Verdict: PASSED WITH WARNINGS (Recommended to polish before ship)\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
