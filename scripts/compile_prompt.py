#!/usr/bin/env python3
# [INPUT]: 依赖一份通过 validate_plan.py 的猫咪身份、视觉性格、表情与特殊材质 sheet plan JSON，以及 references/style-system.md 的固定视觉语法
# [OUTPUT]: 对外提供 backend-neutral 渲染器 prompt；原始 cover-collage 形态、低保真复古拼贴、身份保真与材质可信作为常量写死
# [POS]: scripts 的 prompt 编译器，把每猫性格与每片特殊材质变量嵌回固定的九张 face-in-cover 贴纸骨架，被 SKILL.md 第 5 步调用
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
Asset type: one finished 3:5 portrait die-cut sticker-sheet image for a visual style experiment.
Primary request: transform the single cat in Image 1 into an original retro-pop cover-collage sticker family. The fixed visual mechanism is a photoreal cat-face cutout inserted into an absurd oversized wearable cover shell made from familiar objects and unexpected everyday materials. Keep the playful tension between a believable photographic cat face and a ridiculous object-costume. This is a new original design direction; do not reproduce any existing character, campaign, costume, poster, logo, wording or composition.
Input images: Image 1 is the ONLY cat subject source and the sole authority for every cat trait. Any further image supplies low-fi photomontage medium, tactile material contrast, colour energy and loose poster rhythm ONLY — never its cat, objects, wording, palette mapping or composition. These written rules override every style reference.
No humans, no second cat, no companion, no kitten, no mascot, no extra animal."""

TAIL = """Visual medium: deliberate low-fi photomontage with realistic cat fur, eyes and tactile real-world shell materials; clean but slightly handmade cut-paper edges; high-saturation late-1990s/early-2000s pop-poster energy; simple flat printed highlights; very light halftone and photocopy grain on the cover shells and typography only. The cat face remains clearer and more photographic than the surrounding covers. Keep the page flat and graphic with dry deadpan humour.

Sticker treatment: each of the fifteen pieces carries exactly one continuous pure-white die-cut contour at one identical absolute width across the sheet, about 2% of canvas width. White is the only outline colour. No second outline, coloured rim, halo, glow, bevel, layered edge or cast shadow. Every piece sits fully inside the canvas with visible background gutter between contours; nothing overlaps, touches, merges or clips at an edge.

Facial family and counts: exactly nine main face-in-cover stickers, each containing this same cat exactly once, for exactly nine cat faces on the page. Every face is centered in one clean opening of its cover shell. The six micro-stickers contain no cat. Keep facial identity coherent and the crop face-led; no duplicate face, second head, hidden animal, distorted anatomy, extra eye, missing feature, altered marking, full standing body or seated scene.

Cover-shell rule: all nine pieces keep the same face-in-cover grammar while changing silhouette, opening geometry, material and prop logic. Each oversized shell wraps or replaces the hidden body and fits deliberately around the face, ears, hairline-like fur edge or limited front paws. The material retains believable thickness, texture, reflection, translucency, compression or softness. Absurdity comes from a credible object-material-persona mismatch, not random prop clutter.

Avoid: polished luxury advertising, cinematic lighting, painterly art, 3D renders, glossy toy plastic, smooth vector illustration, anime, chibi, plush or fuzzy mascot anatomy, watercolour, deep cast shadows, sticker packaging, retail mockups, hands holding the sheet, hard equal-cell grids, full-bleed scenery, gradient or textured backgrounds.

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
               "Two large hero covers, four medium covers, three small covers, and six independent micro-stickers in the gaps. "
               "Keep generous visible background gutters.")
    out.append(f"Palette: {', '.join(pg['palette'])}. Overall tone: {pg['mood']}.")
    out.append("")

    out.append("Exactly nine original face-in-cover designs; every row is binding and the inventory is unique to this sheet:")
    for p in sorted(plan["pieces"], key=lambda x: x["n"]):
        out.append(
            f"{p['n']}. {SCALE[p['scale']]} — expression: {p['expression']}. "
            f"Cover shell: {p['object']} remade in {p['material']} ({p['material_class']}), {p['color']}; "
            f"material behaviour: {p['material_behavior']}. Center the same photographic cat face in one clean opening; "
            f"the cover relation is that the cat {VERB[p['mechanism']]} it, displacing the expected {p['displaces']}. "
            f"Physical face-and-ear fit: {p['wearable_fit']}. "
            f"Why it belongs to this cat: {p['persona_fit']}. Absurdity: {p['absurdity']}. "
            f"Crop: {CROP[p['crop']]}"
        )
    out.append("")

    out.append("Exactly six independent micro-stickers in the gaps, each small, cat-free and separately cuttable:")
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
               + "Prohibit every other word, letter, number, logo, watermark, signature, "
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
