<!--
[INPUT]: 依赖已查看的一张猫咪主体图、图片角色标签与用户明确提出的保留项
[OUTPUT]: 对外提供证据受限的猫咪身份锚点、多猫处理和参考图冲突规则，不输出性格判断
[POS]: references 的主体解释层，只回答「这只猫长什么样」，不回答「它是什么性格」
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat Identity

Inspect before writing. Record only traits that are visible or explicitly supplied by the user.

## Record

- filename, available dimensions, image role, and visible cat count;
- user-provided breed, otherwise visible type or `unknown`;
- coat base and major face, muzzle, ear, paw, or body color relationships;
- face mask, patches, stripes, points, or asymmetric markings;
- ear silhouette and distinctive tufts;
- each visible eye color and its viewer-left/viewer-right orientation;
- nose color, broad muzzle shape, and two to four other robust marks;
- every source word, logo, watermark, signature, UI element, and incidental background object to remove.

Do not infer a hidden eye color, obscured marking, pedigree, sex, age, ownership fact, mood, intelligence, obedience, or personality.

## Write The Prompt Identity

Write one compact identity block in the final prompt:

```text
Cat identity: [user-provided breed, visible type, or unknown].
Preserve in all nine depictions: [four to eight visible recognition anchors, including eye and marking orientation when asymmetric].
```

The renderer receives these anchors for all nine cat depictions. Expressions live on individual sticker concepts as acting directions; they are not derived from a personality profile.

## Preservation

Keep across all visible faces:

- broad facial proportions and species;
- coat relationships and defining markings;
- visible eye colors and correct orientation;
- ear silhouette, nose, muzzle, and other robust anchors.

Allow head tilt, crop, limited paw placement, ordinary prop interaction, and mild expression changes. Keep at least four identity anchors readable whenever a prop partially occludes the face.

Never promise exact identity, biometric fidelity, exact pose, exact lighting, or pedigree inferred from appearance. Describe the result as recognition-oriented preservation of visible features.

## Multiple Cats And Reference Conflicts

- If several cats are similarly prominent and no hero is named, ask which cat should lead.
- Never create a pair, group, mirrored self, kitten, or companion to fill inventory.
- The subject source overrides every cat trait in a style reference.
- Remove incidental source text, dates, background objects, watermarks, and UI. Preserve a collar tag only when the user explicitly requests it and its text is clearly legible.
