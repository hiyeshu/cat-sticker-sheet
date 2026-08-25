#!/usr/bin/env python3
# [INPUT]: 依赖一份通过 validate_plan.py 的最小身份、页面、九个日常动作道具与六枚微贴纸 JSON
# [OUTPUT]: 对外提供 backend-neutral 渲染器 Prompt；3:5、9+6、摄影拼贴、单步错位与单层白边作为固定常量
# [POS]: scripts 的 Prompt 编译器，把少量身份、页面与动作道具变量嵌入固定视觉契约
# [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""Compile a validated cat sticker-sheet plan into a renderer prompt.

Usage:
    python3 scripts/compile_prompt.py plan.json [-o prompt.txt]
"""

import argparse
import json
import sys


SCALE = {"hero": "LARGE", "medium": "MEDIUM", "small": "SMALL"}
PRESENTATION = {
    "wears": (
        "The cat wears the object directly; show believable contact with the body part "
        "named in the interaction while keeping the face primary."
    ),
    "operates": (
        "The cat uses the object as a person would; keep the face primary and show only "
        "the front paws required by the action."
    ),
    "face_in_cover": (
        "The cat face appears in one clean opening because this object naturally works "
        "as a hood or cover."
    ),
}

HEAD = """Use case: stylized-concept
Asset type: one finished flat 3:5 portrait die-cut sticker-sheet image.

Primary request: transform the single cat in Image 1 into an original retro-pop photographic prop-collage sticker family. The same realistic cat performs ordinary human actions with familiar everyday objects. Each main sticker contains one simple visual displacement and nothing more. The cuteness comes from a believable cat occupying a recognizable human routine, not from fantasy lore, personality caricature, complicated costumes or random surreal clutter.

Input roles: Image 1 is the ONLY cat subject source and the sole authority for every cat trait. Any additional image supplies low-fi photomontage medium, color energy, loose poster rhythm and border treatment ONLY; never copy its subject, object inventory, wording, palette placement or composition. No human, second cat, kitten, companion, mascot or extra animal."""

TAIL = """One-step rule: keep one primary object and one readable human action in every main sticker. Keep the object's ordinary identity, expected material and familiar construction. Do not combine objects, invent material transformations, add a second joke, assign a fantasy role or build a narrative scene. If an object is handheld, do not turn it into a face shell. If an object naturally forms a hood or cover, use one clean face opening. Keep the cat body hidden or minimally cropped.

Visual medium: deliberate low-fi photomontage with realistic cat fur, eyes and real-world prop textures; clean but slightly handmade cut-paper edges; high-saturation late-1990s/early-2000s pop-poster energy; simple flat printed highlights; very light halftone and photocopy grain on props and optional typography only. Keep the cat face clearer and more photographic than the surrounding collage. Expressions are restrained acting directions, not claims about the cat's personality.

Sticker treatment: every one of the fifteen pieces has exactly one continuous pure-white die-cut contour of the same absolute width, about 2% of canvas width. No second outline, colored rim, halo, glow, bevel, layered edge, cast shadow or photographed paper depth. Every piece is fully inside the canvas with generous visible background gutter; nothing overlaps, touches, merges or clips.

Avoid painterly art, cinematic lighting, 3D rendering, glossy toy plastic, smooth vector illustration, anime, chibi, plush or fuzzy mascot anatomy, watercolor, exaggerated reaction faces, full-body scenes, packaging, retail mockups, screenshots, hands holding the sheet, hard equal-cell grids, full-bleed scenery, gradient or textured backgrounds.

Final output: one flat printable-looking sticker sheet, not separate files."""


def quote(value):
    return f'"{value}"'


def compile_prompt(plan):
    subject = plan["subject"]
    page = plan["page"]
    output = [HEAD, ""]

    output.append(
        f"Cat identity — breed or visible type: {subject['breed_or_type']}. "
        "Preserve these visible anchors in all nine cat depictions: "
        + "; ".join(subject["must_preserve"])
        + ". Keep the cat photographic and recognizable; do not average it into a generic cute cat."
    )
    output.append("")

    output.append(
        f"Canvas: 3:5 portrait, flat front view, one perfectly solid {page['background']} "
        "background with no gradient, vignette, glow, texture, scenery or lighting variation. "
        "Arrange exactly 15 separated pieces: two large main stickers, four medium main "
        "stickers, three small main stickers, and six micro-stickers in the gaps."
    )
    output.append(f"Palette: {', '.join(page['palette'])}.")
    output.append("")

    output.append(
        "Exactly nine main stickers follow. Each contains this same source cat exactly once "
        "and binds one ordinary action to one primary object:"
    )
    for piece in sorted(plan["pieces"], key=lambda item: item["n"]):
        output.append(
            f"{piece['n']}. {SCALE[piece['scale']]} — Human action: {piece['human_action']}. "
            f"Primary object: {piece['object']}, in {piece['color']}. "
            f"Cat interaction: {piece['cat_interaction']}. {PRESENTATION[piece['presentation']]} "
            f"Expression: {piece['expression']}. The one and only displacement is: "
            f"{piece['single_displacement']}. Gentle absurdity level {piece['absurdity_level']} of 2."
        )
    output.append("")

    output.append(
        "Exactly six independent micro-stickers follow. Keep each cat-free, small and separately cuttable:"
    )
    for accent in plan["accents"]:
        if "text" in accent:
            output.append(
                f"{accent['id']}. a short uppercase cut-paper label reading exactly {quote(accent['text'])}."
            )
        else:
            output.append(f"{accent['id']}. {accent['motif']}.")
    output.append("")

    labels = page["text"]
    if labels:
        allowed = " and ".join(quote(label) for label in labels)
        output.append(
            f"Text: only {allowed} may appear, spelled exactly as quoted. "
            "Allow no other word, letter, number, logo, watermark, signature, account name, "
            "speech bubble, garment label or gibberish."
        )
    else:
        output.append(
            "Text: no text anywhere. Allow no word, letter, number, logo, watermark, signature, "
            "account name, speech bubble, garment label or gibberish."
        )
    output.append("")
    output.append(TAIL)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    parser.add_argument("-o", "--out")
    args = parser.parse_args()

    with open(args.plan, encoding="utf-8") as handle:
        prompt = compile_prompt(json.load(handle))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(prompt + "\n")
        print(f"已写出 {args.out}（{len(prompt.split())} 词）")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
