#!/usr/bin/env python3
# [INPUT]: 依赖 references/sheet.schema.json 的最小字段契约与 one-step-concepts.md 的单步错位规则
# [OUTPUT]: 对外提供出图前结构闸门：9+6、2/4/3、编号、动作/道具/错位唯一性、呈现方式与文字一致性
# [POS]: scripts 的计划校验器，只检查能稳定机器判定且直接影响画面的结构字段，把语义效果留给视觉质量门
# [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""Validate one cat sticker-sheet plan.

Usage:
    python3 scripts/validate_plan.py plan.json

Exit 0 means accepted; exit 1 means rejected.
"""

import argparse
import collections
import json
import os
import re
import sys


SCALE_QUOTA = {"hero": 2, "medium": 4, "small": 3}
EMPTY_DISPLACEMENTS = {
    "", "-", "none", "nothing", "n/a", "无", "没有", "普通", "正常", "随便"
}
MULTI_IDEA_MARKERS = (
    " and also ", " plus ", " as well as ", "同时", "以及", "并且", "外加", "兼具"
)
TOP_FIELDS = ("subject", "page", "pieces", "accents")
SUBJECT_FIELDS = ("breed_or_type", "must_preserve")
PAGE_FIELDS = ("background", "palette", "text")
PIECE_FIELDS = (
    "n", "scale", "presentation", "human_action", "object", "cat_interaction",
    "single_displacement", "expression", "color", "absurdity_level"
)


def normalize(value):
    """Normalize short concept labels for exact within-sheet duplicate checks."""
    return re.sub(r"\s+", " ", value.strip().casefold())


def check_minimum_contract(plan):
    """Validate the compact contract without external packages."""
    errors = []
    if not isinstance(plan, dict):
        return ["root 必须是 JSON object"]
    for key in TOP_FIELDS:
        if key not in plan:
            errors.append(f"缺少顶层字段: {key}")
    if errors:
        return errors
    unexpected = sorted(set(plan) - set(TOP_FIELDS))
    if unexpected:
        errors.append(f"不支持的顶层字段: {', '.join(unexpected)}")

    subject = plan["subject"]
    page = plan["page"]
    pieces = plan["pieces"]
    accents = plan["accents"]
    if not isinstance(subject, dict):
        errors.append("subject 必须是 object")
    else:
        for key in SUBJECT_FIELDS:
            if key not in subject:
                errors.append(f"subject 缺少字段: {key}")
        extra = sorted(set(subject) - set(SUBJECT_FIELDS))
        if extra:
            errors.append(f"subject 不支持字段: {', '.join(extra)}")
        if not isinstance(subject.get("breed_or_type"), str) or not subject.get("breed_or_type", "").strip():
            errors.append("subject.breed_or_type 必须是非空字符串")
        anchors = subject.get("must_preserve")
        if not isinstance(anchors, list) or not 4 <= len(anchors) <= 8:
            errors.append("subject.must_preserve 必须包含 4–8 个身份锚点")
        elif any(not isinstance(anchor, str) or not anchor.strip() for anchor in anchors):
            errors.append("subject.must_preserve 每项必须是非空字符串")
        elif len(set(anchors)) != len(anchors):
            errors.append("subject.must_preserve 不得重复")
    if not isinstance(page, dict):
        errors.append("page 必须是 object")
    else:
        for key in PAGE_FIELDS:
            if key not in page:
                errors.append(f"page 缺少字段: {key}")
        extra = sorted(set(page) - set(PAGE_FIELDS))
        if extra:
            errors.append(f"page 不支持字段: {', '.join(extra)}")
        if not isinstance(page.get("background"), str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", page.get("background", "")):
            errors.append("page.background 必须是 #RRGGBB")
        palette = page.get("palette")
        if not isinstance(palette, list) or not 3 <= len(palette) <= 6:
            errors.append("page.palette 必须包含 3–6 个颜色")
        elif any(not isinstance(color, str) or not color.strip() for color in palette):
            errors.append("page.palette 每项必须是非空字符串")
        elif len(set(palette)) != len(palette):
            errors.append("page.palette 不得重复")
        text = page.get("text")
        if not isinstance(text, list) or len(text) > 2:
            errors.append("page.text 必须是最多 2 项的数组")
        elif any(not isinstance(label, str) or not label.strip() for label in text):
            errors.append("page.text 每项必须是非空字符串")
        elif len(set(text)) != len(text):
            errors.append("page.text 不得重复")
    if not isinstance(pieces, list):
        errors.append("pieces 必须是 array")
    else:
        for index, piece in enumerate(pieces, 1):
            if not isinstance(piece, dict):
                errors.append(f"pieces[{index}] 必须是 object")
                continue
            missing = [key for key in PIECE_FIELDS if key not in piece]
            if missing:
                errors.append(f"pieces[{index}] 缺少字段: {', '.join(missing)}")
                continue
            extra = sorted(set(piece) - set(PIECE_FIELDS))
            if extra:
                errors.append(f"pieces[{index}] 不支持字段: {', '.join(extra)}")
            if type(piece["n"]) is not int:
                errors.append(f"pieces[{index}].n 必须是整数")
            if not isinstance(piece["scale"], str) or piece["scale"] not in SCALE_QUOTA:
                errors.append(f"pieces[{index}].scale 无效: {piece['scale']}")
            if not isinstance(piece["presentation"], str) or piece["presentation"] not in {"wears", "operates", "face_in_cover"}:
                errors.append(f"pieces[{index}].presentation 无效: {piece['presentation']}")
            for field in ("human_action", "object", "cat_interaction", "single_displacement", "expression", "color"):
                if not isinstance(piece[field], str) or not piece[field].strip():
                    errors.append(f"pieces[{index}].{field} 必须是非空字符串")
            if type(piece["absurdity_level"]) is not int or piece["absurdity_level"] not in {1, 2}:
                errors.append(f"pieces[{index}].absurdity_level 只能是 1 或 2")
    if not isinstance(accents, list):
        errors.append("accents 必须是 array")
    else:
        for index, accent in enumerate(accents, 1):
            if not isinstance(accent, dict) or "id" not in accent:
                errors.append(f"accents[{index}] 必须是含 id 的 object")
            elif ("motif" in accent) == ("text" in accent):
                errors.append(f"accents[{index}] 必须且只能包含 motif 或 text 之一")
            elif set(accent) - {"id", "motif", "text"}:
                errors.append(f"accents[{index}] 包含不支持字段")
            elif any(not isinstance(value, str) or not value.strip() for value in accent.values()):
                errors.append(f"accents[{index}] 的值必须是非空字符串")
    return errors


def duplicate_errors(pieces, field, label):
    """Return explicit duplicate errors for a concept-bearing field."""
    seen = {}
    errors = []
    for piece in pieces:
        value = normalize(piece[field])
        if value in seen:
            errors.append(
                f"#{piece['n']} 与 #{seen[value]} 的{label}重复: {piece[field]}"
            )
        else:
            seen[value] = piece["n"]
    return errors


def check_structure(plan):
    """Check only constraints that are simple, observable, and presentation-critical."""
    errors = []
    warnings = []
    pieces = plan["pieces"]
    accents = plan["accents"]

    if len(pieces) != 9:
        errors.append(f"主贴纸 {len(pieces)} 片，应为 9")
    if len(accents) != 6:
        errors.append(f"微贴纸 {len(accents)} 枚，应为 6")

    numbers = sorted(piece["n"] for piece in pieces)
    if numbers != list(range(1, 10)):
        errors.append(f"pieces.n 应恰好为 1–9，当前为 {numbers}")

    scales = collections.Counter(piece["scale"] for piece in pieces)
    actual_scales = {name: scales.get(name, 0) for name in SCALE_QUOTA}
    if actual_scales != SCALE_QUOTA:
        errors.append(
            f"尺度配额 {actual_scales}，应为 hero 2 / medium 4 / small 3"
        )

    presentations = {piece["presentation"] for piece in pieces}
    if len(presentations) < 2:
        errors.append("九片只使用一种呈现方式；至少混合 wears / operates / face_in_cover 中两种")

    errors.extend(duplicate_errors(pieces, "human_action", "人类动作"))
    errors.extend(duplicate_errors(pieces, "object", "主道具"))
    errors.extend(duplicate_errors(pieces, "single_displacement", "错位点"))

    for piece in pieces:
        displacement = normalize(piece["single_displacement"])
        if displacement in EMPTY_DISPLACEMENTS:
            errors.append(f"#{piece['n']} 的 single_displacement 没有说明唯一错位")
        if any(marker in f" {displacement} " for marker in MULTI_IDEA_MARKERS):
            warnings.append(
                f"#{piece['n']} 的 single_displacement 可能包含多个笑点，请确认只保留一个"
            )

    expressions = {normalize(piece["expression"]) for piece in pieces}
    if len(expressions) < 3:
        warnings.append(f"九片只有 {len(expressions)} 种表情；可轻微变化，但不要改成人格分类")

    for color, count in collections.Counter(piece["color"] for piece in pieces).items():
        if count > 4:
            warnings.append(f"主色「{color}」出现 {count} 次，可能削弱贴纸间辨识度")

    accent_ids = [accent["id"] for accent in accents]
    if len(set(accent_ids)) != len(accent_ids):
        errors.append("accents.id 存在重复")

    accent_text = sorted(accent.get("text", "") for accent in accents if "text" in accent)
    page_text = sorted(plan["page"]["text"])
    if accent_text != page_text:
        errors.append(f"微贴纸文字 {accent_text} 与 page.text {page_text} 不一致")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    args = parser.parse_args()

    with open(args.plan, encoding="utf-8") as handle:
        plan = json.load(handle)

    errors = check_minimum_contract(plan)
    warnings = []

    if not errors:
        structure_errors, structure_warnings = check_structure(plan)
        errors.extend(structure_errors)
        warnings.extend(structure_warnings)

    print(f"== {os.path.basename(args.plan)} ==")
    for error in errors:
        print("  ✗", error)
    for warning in warnings:
        print("  !", warning)
    print(f"\n{'拒收' if errors else '通过'}：{len(errors)} 项硬伤 / {len(warnings)} 项提示")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
