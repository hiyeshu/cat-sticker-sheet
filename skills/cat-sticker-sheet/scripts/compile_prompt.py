#!/usr/bin/env python3
# [INPUT]: 依赖一份通过 validate_plan.py 的猫咪身份、视觉性格、表情与特殊材质 sheet plan JSON，以及 references/style-system.md 的固定视觉语法
# [OUTPUT]: 对外提供 backend-neutral 渲染器 prompt；猫头优先、身份保真、材质可信和反向约束作为常量写死在本文件
# [POS]: scripts 的 prompt 编译器，把每猫性格与每片荒诞穿戴变量编译成一张一致的贴纸版，被 SKILL.md 第 5 步调用
# [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""用法:
    python3 scripts/compile_prompt.py plan.json [-o out.txt]

常量只写在这里一次。JSON 只提供变量。
IP 边界不进本文件的输出——对渲染器点名一个品牌，等于把它放进条件里。
"""
import argparse, json, sys

VERB = {
    "becomes_part":        "becomes a working part of",
    "replaces_silhouette": "replaces the body of",
    "wraps":               "is wrapped by",
    "wears":               "wears",
    "operates":            "works the controls of",
    "spills_from":         "spills out of",
    "peeks_through":       "is seen through",
    "nests":               "nests inside",
    "face_window":         "fills the one opening of",
}
SCALE = {"hero": "LARGE", "medium": "MEDIUM", "small": "SMALL"}
CROP = {
    "face":      "head only, ears readable",
    "face_ears": "head only with both ears fully readable",
    "face_paws": "head with only the front paws entering the composition",
    "head_shoulders": "head and a minimal shoulder crop, never a full body",
}

HEAD = """Use case: stylized-concept
Asset type: one finished 3:5 portrait die-cut sticker-sheet image.
Primary request: transform the single cat in Image 1 into an original photoreal cut-paper collage family of exactly nine cat-head stickers with surreal wearables, face frames or compact paw interactions, plus exactly six tiny accent stickers, all on one page.
Input images: Image 1 is the ONLY cat subject source and the sole authority for every cat trait. Any further image supplies collage medium, material contrast, colour energy and loose page rhythm ONLY — never its cat, its objects, its wording, its palette mapping or its composition. These written rules override every style reference.
No humans, no second cat, no companion, no kitten, no mascot, no extra animal."""

TAIL = """Style and medium: photoreal cut-paper photomontage. The cat's real fur and natural eyes stay sharper and more photographic than the wearable constructions around them. Tactile real-world materials, high-saturation retro colour blocking, slightly imperfect hand-cut outer contours, restrained internal photographic depth, dry deadpan humour. Keep the page flat and graphic.

Sticker treatment: each of the fifteen pieces carries exactly one continuous pure-white die-cut contour at one identical absolute width across the sheet, about 2% of canvas width. White is the only outline colour. No second outline, coloured rim, halo, glow, bevel, layered edge or cast shadow. Every piece sits fully inside the canvas with visible background gutter between contours; nothing overlaps, touches, merges or clips at an edge.

Counts: exactly nine main stickers, each containing exactly one head depiction of this same cat, for exactly nine cat heads on the page. The six accents contain no cat. Keep every main piece face-led; no full standing or seated bodies. No duplicate face, second head, extra eye, missing eye, extra limb or altered markings.

Wearable rule: every object must perch on, wrap, frame, reshape, reveal or be worked by the cat's head, ears or front paws. Fit follows the skull and ears with visible pressure, folds, openings or balance. The special material must retain believable thickness, texture, reflection, translucency or softness. Absurdity comes from a credible object-material-persona mismatch, not random prop clutter. The same construction repeated across the page fails.

Avoid: hand-drawn line art, watercolour, crayon, painterly rendering, anime, vector-perfect icons, plush or fuzzy mascot anatomy, clay, glossy 3D toy renders, airbrush gradients, cinematic or studio lighting, deep cast shadows, luxury advertising polish, sticker packaging, retail mockups, hands holding the sheet, hard equal-cell grids, full-bleed scenery, gradient or textured backgrounds.

Final output: one flat printable sticker sheet. Not packaging, not a retail mockup, not a screenshot, not separate files."""


def compile_prompt(plan):
    s, pg = plan["subject"], plan["page"]
    vp = s["visual_persona"]
    q = lambda w: '"' + w + '"'
    out = [HEAD, ""]

    out.append(f"Cat identity — breed or visible type: {s['breed_or_type']}. "
               "Preserve these anchors in every visible face: "
               + "; ".join(s["must_preserve"]) + ". "
               "Keep the cat photographic and recognisable; do not average it into a generic cute cat.")
    out.append(
        f"Visual persona — primary: {vp['primary']}; secondary: {', '.join(vp['secondary'])}; "
        f"energy: {vp['energy_level']}. Expression language: {'; '.join(vp['expression_language'])}. "
        f"Avoid expressions that imply: {'; '.join(vp['avoid_expressions'])}. "
        "This is an image-based character impression, not a claim about the animal's real temperament."
    )
    out.append("")

    out.append(f"Canvas: 3:5 portrait, flat front view, one perfectly clean solid {pg['background']} field — "
               "no gradient, vignette, glow, texture, pattern, scenery or lighting variation. "
               f"Arrange exactly 15 separate pieces in this rhythm: {pg['layout']}. "
               "Two large hero portraits, four medium portraits, three small portraits, six smaller accents. "
               "Keep generous visible background gutters.")
    out.append(f"Palette: {', '.join(pg['palette'])}. Overall tone: {pg['mood']}.")
    out.append("")

    out.append("Nine cat-head concepts; every row is binding and the examples are not reusable inventory:")
    for p in sorted(plan["pieces"], key=lambda x: x["n"]):
        out.append(
            f"{p['n']}. {SCALE[p['scale']]} — expression: {p['expression']}. "
            f"Concept: {p['object']} remade in {p['material']} ({p['material_class']}), {p['color']}; "
            f"material behaviour: {p['material_behavior']}. The cat {VERB[p['mechanism']]} it, "
            f"displacing the expected {p['displaces']}. Physical cat fit: {p['wearable_fit']}. "
            f"Why it belongs to this cat: {p['persona_fit']}. Absurdity: {p['absurdity']}. "
            f"Crop: {CROP[p['crop']]}"
        )
    out.append("")

    out.append("Six accent stickers, each small, cat-free and separately cuttable:")
    for a in plan["accents"]:
        if "text" in a:
            out.append(f"{a['id']}. a short hand-cut uppercase label reading exactly {q(a['text'])}.")
        else:
            src = f" (left behind by piece {a['residue_of']})" if "residue_of" in a else ""
            out.append(f"{a['id']}. {a['motif']}{src}.")
    out.append("")

    t = pg["text"]
    out.append("Text: " + (f"only {' and '.join(q(w) for w in t)} may appear, spelled exactly as quoted. "
                           if t else "no text at all anywhere. ")
               + "Prohibit every other word, letter, number, logo, brand, watermark, signature, "
                 "speech bubble and gibberish.")
    out.append("")
    out.append(TAIL)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    text = compile_prompt(json.load(open(a.plan, encoding="utf-8")))
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text + "\n")
        print(f"已写出 {a.out}（{len(text.split())} 词）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
