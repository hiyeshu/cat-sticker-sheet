<!--
[INPUT]: 依赖已查看的一张猫咪主体图、图片角色标签和用户明确提出的保留项
[OUTPUT]: 对外提供可验证的猫咪视觉基因、证据受限的 visual_persona、must_preserve 与 generative_cue、多猫处理与锚点冲突规则
[POS]: references 的输入解释层，确保目标猫的外貌与视觉角色气质共同驱动九张猫头贴纸，且风格锚点不能改写身份
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat Subject Genome

Inspect before interpreting. Record only visible evidence; label visual persona as inferred. A photo can support a character impression, never a claim about the animal's real temperament.

## Inspect The Source

Record:

- filename and available dimensions;
- image role and visible cat count;
- coat base color and value pattern;
- face mask, patches, stripes, points, socks, chest, or muzzle markings;
- ear silhouette, size, angle, and distinctive tufts;
- eye color for each visible eye, including heterochromia orientation;
- nose color and broad muzzle shape;
- two to four additional distinctive marks and any user-provided breed; otherwise record only visible type and write `unknown` rather than guessing pedigree;
- source pose, crop, visible paws/body, eyelid openness, gaze direction, mouth tension, ear stance, head posture, and one inferred visual persona;
- every word, logo, signature, watermark, UI element, and incidental background object.

Do not infer a hidden eye color, obscured marking, breed, sex, age, ownership fact, or real personality.

## Write The Genome JSON

Use this record and replace every placeholder:

```json
{
  "subject_count": 1,
  "species": "cat",
  "breed_or_type": "user-provided breed, visible type, or unknown",
  "coat": {
    "base": "observed color",
    "face_mask": "observed pattern or none",
    "body_markings": ["observed marking"]
  },
  "ears": "observed silhouette",
  "eyes": {
    "viewer_left": "observed color or not visible",
    "viewer_right": "observed color or not visible",
    "orientation_lock": "frontal viewer orientation or anatomical side when known"
  },
  "nose_and_muzzle": "observed color and broad shape",
  "distinctive_marks": ["two to four robust anchors"],
  "must_preserve": ["four to six visible recognition anchors"],
  "visual_persona": {
    "primary": "one image-based character impression",
    "secondary": ["one to three supporting qualities"],
    "energy_level": "low, medium, or high",
    "expression_language": ["three to six facial behaviors compatible with this face"],
    "avoid_expressions": ["one to four expressions that would turn it into another character"]
  },
  "generative_cue": "which visible trait or persona cue of THIS cat should drive objects, expressions, or materials",
  "may_vary": ["head crop", "ear interaction", "paw visibility", "wearable fit", "persona-consistent expression"],
  "must_not_appear": ["extra cat", "duplicate head", "style-anchor cat traits", "unapproved text"]
}
```

`breed_or_type`、`must_preserve`、`visual_persona` 与 `generative_cue` 直接进入 sheet plan 的 `subject` 字段，契约见 `sheet.schema.json`。

## 基因有两种用法

`must_preserve` 是**保真约束**：这些锚点必须活着穿过九片。

`visual_persona` 是**角色约束**：萌、呆憨、乖巧、机灵只是可能的外观读法，不是固定分类。主气质决定表情语法，辅助气质提供变化；`avoid_expressions` 防止一张温顺慢热的脸突然被画成夸张狡猾的通用表情包。

`generative_cue` 是**生成燃料**：这只猫的哪个外貌或气质特征应当决定物件、表情或材质。不可省略——省了，整页就退化成「任何一只同色猫都成立」的通用世界。

- 异色瞳 → 优先选本身成对、但两边本不该不同的物件；
- 长毛 → 优先选会被毛填满或溢出的物件；
- 圆脸 → 优先选能顺着圆形脸缘受力的框、罩、环或读数面；
- 深色面罩 → 优先选带独立面板、开口或取景框的结构；
- 呆憨的低能量视觉气质 → 让荒诞材料承担笑点，表情保持慢半拍；
- 机灵的高能量视觉气质 → 允许侧眼、挑眉式眼睑变化和更主动的前爪互动，但不能改画眼型。

至少三片的物件/材料必须由可见基因推出，至少六片的表情与情境必须符合 `visual_persona`。**换一只猫就不成立**。做到这一点，最脆弱的锚点与性格印象就从「要记得检查的项」变成整页的地基。

如何把它变成九个槽位，见 `shell-variation.md`。

## Preservation Contract

Retain across all visible faces:

- species and broad facial proportions;
- coat base and the major relationship between face, muzzle, ears, paws, and body colors;
- eye colors and orientation when they are visible in the source;
- ear silhouette, nose color, muzzle relationship, and defining marks;
- the source's broad visual persona, especially its habitual eyelid, gaze, ear and mouth relationships.

Allow:

- new head crop, scale, head tilt, ear interaction, limited paw placement, and wearable opening;
- distinct expressions selected from the persona's expression language without redrawing the face;
- partial occlusion by an object when at least four anchors remain readable;
- new special materials and page colors.

Never promise exact identity, biometric fidelity, exact pose, exact photographic lighting, pedigree inferred from appearance, or the cat's true personality. Report the result as recognition-oriented preservation of visible anchors plus an image-based visual persona.

## Multiple Cats

- If one cat is clearly dominant and the user explicitly identifies it, use only that cat and prohibit all others.
- If several cats are similarly prominent and no hero is named, ask which cat should lead.
- Do not create group, pair, mirrored-self, kitten, or companion stickers to fill inventory.

## Resolve Anchor Conflicts

The user's subject source wins every conflict. The bundled yellow image contributes no coat color, eye color, mask, ear shape, nose, expression, body pattern, or breed cue. Explicitly prohibit the anchor cat's traits whenever they differ from the target genome.

Remove all incidental source text, logos, background objects, dates, account names, watermarks, and UI. Preserve a subject-attached collar tag or label only when the user explicitly requests it and the wording is clearly legible.
