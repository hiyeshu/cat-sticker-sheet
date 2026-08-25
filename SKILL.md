---
name: cat-sticker-sheet
description: >-
  Turn one supplied cat photo or clear cat illustration into a finished 3:5
  retro-pop photographic collage sticker sheet with nine face-led cat stickers
  performing ordinary human actions with familiar props, plus six micro-stickers.
  Use for 猫头贴纸, 猫咪表情贴纸, pet sticker sheets, lightly absurd anthropomorphic
  cat stickers, or a prompt-only recipe for this look. Preserve visible breed/type
  and identity anchors; create cuteness through one simple everyday displacement
  per sticker without inferring the cat's personality or inventing fantasy lore.
---

<!--
[INPUT]: 依赖一张清晰单猫主体图、references/ 的身份/日常错位/视觉规则、优先使用的原生生图工具，以及仅在原生生图工具缺席时启用的 GD CLI 兜底
[OUTPUT]: 对外提供一张 3:5 复古摄影拼贴猫咪贴纸版、实际使用的最终 Prompt 与视觉质量结论
[POS]: cat-sticker-sheet 的单一执行入口；只保留「真实猫身份 + 普通人类道具/行为 + 一个轻微错位」所需规则，防止性格臆测、复杂世界观和过度荒诞
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat Sticker Sheet

Turn one real cat into a retro-pop photographic sticker family. The cat stays recognizable; ordinary human props and routines create the joke.

## Hold The Contract

- Produce one flat 3:5 portrait sheet: exactly **9 main stickers + 6 micro-stickers**.
- Arrange the main stickers as **2 large + 4 medium + 3 small** with six separated micro-stickers in the gaps.
- Show the same source cat exactly once in every main sticker and nowhere in the micro-stickers. Keep the face photographic and the body hidden or minimally cropped.
- Preserve visible breed/type, coat relationships, face markings, ear silhouette, eye colors and orientation, nose, muzzle, and distinctive marks. Never guess pedigree or promise biometric identity.
- Do not infer whether the cat is cute, goofy, obedient, clever, aloof, or any other personality. Expressions are temporary acting directions, not character diagnosis.
- Build each main sticker from one recognizable human action, one familiar primary object, and one simple displacement. If the joke needs more than one sentence to explain, simplify it.
- Keep the object recognizable, normally constructed, and materially believable. Do not add an unexpected material, second prop, fantasy role, or secondary gag unless the user explicitly asks.
- Let the prop be worn, held, or operated. Use a clean face opening only when the object naturally forms a hood, cover, bag, towel, or shell; do not force telephones, cups, or handheld tools into face windows.
- Treat telephone calls, a black plastic bag used as a hood, a baseball cap, a bath towel, or drinking coffee as calibration examples, never a mandatory inventory.
- Use deliberate low-fi photomontage, high-saturation late-1990s/early-2000s poster energy, a background treatment chosen for this sheet, and one pure-white die-cut contour around every piece.
- Permit zero to two short labels. Quote approved text exactly and allow no other words, logos, watermarks, signatures, account names, or gibberish.
- Use a callable native image-generation tool whenever one is available. Use GD CLI only when the runtime exposes no native image-generation tool at all; a failed, slow, rate-limited, or unsatisfactory native call does not count as tool absence.

## Route The Request

- **Generate — default:** inspect the cat, write the final prompt, generate, inspect, correct once if needed, and return the selected sheet plus the exact prompt used.
- **Prompt-only:** write the same final prompt, but do not claim that an image was generated or inspected.
- **Missing source:** ask for the cat image when the request points to “this cat” but no usable image exists.
- **Multiple cats:** ask which cat should lead when the source does not have one unambiguous subject. Never mix several cats on one sheet.
- **Batch:** make one independent sheet per supplied single-cat image.

Assign every input one role:

- **Subject source:** the only authority for cat identity and the only cat included in generation.
- **User style reference:** may supply medium, palette, or layout cues, never another subject or copied inventory.

## Load Only What Is Needed

- Read `references/style-system.md` for every request.
- Read `references/subject-identity.md` when an image is supplied.
- Read `references/one-step-concepts.md` before writing the nine concepts.
- Read `references/quality-gate.md` before returning a generated result.
- Read `references/gd-cli.md` only after confirming that the runtime exposes no callable native image-generation tool. Do not load or use it while a native tool is available.

Resolve bundled paths relative to this `SKILL.md`.

## Generate

1. **Inspect the source.** Record one subject count and four to eight robust identity anchors. Treat unreadable or hidden traits as unknown.
2. **Write the final prompt.** State the identity anchors, background direction, palette, 3:5 format, 2/4/3 scale rhythm, nine distinct action-object-interaction-displacement-expression concepts, six cat-free micro-stickers, single white contour, and text boundary. Keep it backend-neutral and placeholder-free; do not create a separate plan artifact.
3. **Choose the renderer.** Apply the native-first rule above; use `references/gd-cli.md` only for fallback.
4. **Generate from the real source.** Pass only user-provided or task-required images, with the subject first. On the native route, use `referenced_image_paths` for local inputs or the smallest sufficient `num_last_images_to_include` for conversation-only inputs; never use both mechanisms. On the GD CLI fallback route, follow `references/gd-cli.md`. Never pass the bundled anchor to any renderer.
5. **Inspect.** Apply `references/quality-gate.md` to the actual image. Regenerate once with one targeted correction if it fails, using the already-selected renderer only.
6. **Return honestly.** Return the selected image, exact final prompt, visual review result, and one precise remaining limitation if any. Save project-bound outputs under `output/cat-sticker-sheets/`, never inside the installed Skill.

## Return Shape

````markdown
**猫咪贴纸排版图**

![Cat sticker sheet](absolute-image-path-or-rendered-image)

**最终 Prompt**

```text
[exact final prompt]
```

**说明**

- Mode: [Generate / Prompt-only]
- Cat identity: [visible type + preserved anchors]
- Visual review: [pass, fail, or not run]
- Quality: [pass, corrected once, or one precise limitation]
````

## Non-negotiable Outcome

The result must read in one glance: the same real cat, nine ordinary human situations, one gentle wrongness per situation, six small accents, and one cohesive flat sticker sheet. The cat-object mismatch creates the cuteness; complexity does not.
