<!--
[INPUT]: 依赖实际生成的 raster、通过校验的最小 sheet plan JSON，以及 scripts/audit_sheet.py 的机器判定
[OUTPUT]: 对外提供机器闸门、九片单步错位视觉枚举、纠正规则与诚实降级规则
[POS]: references 的最终质量门；机器检查几何，眼睛只检查身份、动作可读性和轻微荒诞是否成立
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Quality Gate

## Machine Gate

Run first:

```bash
python3 <skill-dir>/scripts/audit_sheet.py <image>
```

It checks the 3:5 aspect, background separation, 15 separated components, bleed, gutters, white contours, and contour-width consistency. A nonzero exit is a rejection, not a warning to ignore.

## Visual Gate

Inspect the actual image and enumerate all nine main stickers:

| # | human action × object | presentation | one visible displacement | preserved identity anchors |
|---|---|---|---|---|

Then verify:

- Exactly nine cat depictions, one per main sticker; the six micro-stickers contain no cat.
- The main scale rhythm reads as 2 large / 4 medium / 3 small, with six separate micro-stickers in the gaps.
- At least eight cat faces clearly preserve the declared coat, markings, ears, eyes, nose, and muzzle. Asymmetric eyes or markings keep the correct orientation.
- Every human action and primary object is recognizable at a glance.
- Every main sticker contains one understandable wrongness, not a fantasy scene, compound costume, material stunt, or pile of unrelated props.
- Objects retain their expected material and physical behavior unless the user explicitly requested otherwise.
- Expressions remain natural acting cues and do not turn the cat into nine unrelated cartoon personalities.
- Worn items fit the head; operated items show only necessary paws; face openings appear only on objects that naturally form covers.
- The result remains photographic low-fi collage, not 3D toy art, anime, chibi, plush, watercolor, or smooth vector illustration.
- All fifteen pieces have one white contour and remain separated. The background supports the sheet's palette and cute effect without swallowing the visible gutters or white-contour contrast.
- Zero to two approved labels are spelled exactly; no extra words, logos, watermarks, signatures, account names, or gibberish appear.

## Correct Once

If either gate fails, regenerate once with one targeted correction. Repeat the source-cat identity, 9+6 count, 2/4/3 rhythm, affected action-object concept, one-displacement rule, background direction, and single white contour. Do not add a new concept while fixing another.

Prioritize: wrong subject or extra cat; wrong counts or merged pieces; lost identity; unreadable action; multiple jokes in one sticker; style drift; border or text defects.

If the second result still fails, return the better image and name the exact remaining defect.

## Honesty

- Do not claim a machine pass unless the script returned zero.
- If visual inspection is unavailable, downgrade to prompt-only and say so.
- Do not report eight cat faces as nine, a nearby prop as interaction, or a complex scene as one-step absurdity.

For prompt-only delivery, require a passing plan, a placeholder-free compiled prompt, explicit identity anchors, nine action-object concepts, six micro-stickers, counts, background, and border constraints. State that no image was generated or visually inspected.
