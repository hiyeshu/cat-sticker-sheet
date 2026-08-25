<!--
[INPUT]: 依赖实际生成的图片、最终 Prompt 与用户猫咪主体图
[OUTPUT]: 对外提供九片身份/动作/单错位和整页几何的视觉枚举、一次纠正规则与诚实降级规则
[POS]: references 的最终质量门，以直接视觉检查判断身份、动作、数量、几何和轻微荒诞是否成立
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Quality Gate

## Inspect The Image

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

If the image fails this review, regenerate once with one targeted correction. Repeat the source-cat identity, 9+6 count, 2/4/3 rhythm, affected action-object concept, one-displacement rule, background direction, and single white contour. Do not add a new concept while fixing another.

Prioritize: wrong subject or extra cat; wrong counts or merged pieces; lost identity; unreadable action; multiple jokes in one sticker; style drift; border or text defects.

If the second result still fails, return the better image and name the exact remaining defect.

## Honesty

- If visual inspection is unavailable, downgrade to prompt-only and say so.
- Do not report eight cat faces as nine, a nearby prop as interaction, or a complex scene as one-step absurdity.

For prompt-only delivery, require a placeholder-free final prompt with explicit identity anchors, nine action-object concepts, six micro-stickers, counts, background, and border constraints. State that no image was generated or visually inspected.
