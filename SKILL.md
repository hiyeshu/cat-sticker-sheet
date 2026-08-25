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
[INPUT]: 依赖一张清晰单猫主体图、assets/yellow-cat-collage-anchor.png 的次级媒介线索、references/ 的身份/日常错位/视觉规则、scripts/ 的校验与编译器，以及内置 image_gen 能力
[OUTPUT]: 对外提供一张 3:5 复古摄影拼贴猫咪贴纸版、最小 sheet plan JSON、最终 Prompt 与可验证的质量结论
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
- Use deliberate low-fi photomontage, high-saturation late-1990s/early-2000s poster energy, a perfectly flat solid background, and one pure-white die-cut contour around every piece.
- Permit zero to two short labels. Quote approved text exactly and allow no other words, logos, watermarks, signatures, account names, or gibberish.
- Use built-in image generation by default. Do not silently switch renderers.

## Route The Request

- **Generate — default:** inspect the cat, plan nine one-step concepts, validate, compile, generate, inspect, correct once if needed, and return the selected sheet plus its plan and prompt.
- **Prompt-only:** validate and compile the same plan, but do not claim that an image was generated or inspected.
- **Missing source:** ask for the cat image when the request points to “this cat” but no usable image exists.
- **Multiple cats:** ask which cat should lead when the source does not have one unambiguous subject. Never mix several cats on one sheet.
- **Batch:** make one independent sheet per supplied single-cat image.

Assign every input one role:

- **Subject source:** the only authority for cat identity and the only cat included in generation.
- **Bundled anchor:** `assets/yellow-cat-collage-anchor.png`; supplies photographic collage, color energy, loose rhythm, and border treatment only.
- **User style reference:** may supply medium, palette, or layout cues, never another subject or copied inventory.

## Load Only What Is Needed

- Read `references/style-system.md` for every request.
- Read `references/subject-identity.md` when an image is supplied.
- Read `references/one-step-concepts.md` before planning the nine concepts.
- Follow `references/sheet.schema.json` when writing the plan.
- Read `references/quality-gate.md` before returning a generated result.

Use the scripts instead of reproducing their rules in prose:

- `scripts/validate_plan.py` validates counts, scale rhythm, uniqueness, and one-step displacement.
- `scripts/compile_prompt.py` turns the plan into the renderer prompt.
- `scripts/audit_sheet.py` checks the generated raster's aspect, background, piece count, spacing, and white contours.

Resolve bundled paths relative to this `SKILL.md`.

## Generate

1. **Inspect the source.** Record one subject count and four to eight robust identity anchors. Treat unreadable or hidden traits as unknown.
2. **Write the plan.** Use the schema: subject identity, page colors, nine ordinary action-object concepts, and six micro-stickers. Give every main sticker one `human_action`, one `object`, one `cat_interaction`, one `single_displacement`, and a natural `expression`.
3. **Validate.** Run `python3 <skill-dir>/scripts/validate_plan.py <plan.json>`. Fix rejected fields; do not bypass the gate.
4. **Compile.** Run `python3 <skill-dir>/scripts/compile_prompt.py <plan.json>`. Use the compiled text unchanged.
5. **Generate from the real source.** When all inputs have local paths, pass the subject first and bundled anchor second through `referenced_image_paths`. When the subject exists only in conversation, include the smallest sufficient number of recent images and restate the written style. Never use both image-input mechanisms.
6. **Inspect.** Run `python3 <skill-dir>/scripts/audit_sheet.py <image>`, then apply `references/quality-gate.md`. Regenerate once with one targeted correction if either gate fails.
7. **Return honestly.** Return the selected image, plan JSON, exact compiled prompt, gate results, and one precise remaining limitation if any. Save project-bound outputs under `output/cat-sticker-sheets/`, never inside the installed Skill.

## Return Shape

````markdown
**猫咪贴纸排版图**

![Cat sticker sheet](absolute-image-path-or-rendered-image)

**计划 JSON**

```json
{...}
```

**最终 Prompt**

```text
[exact compiled prompt]
```

**说明**

- Mode: [Generate / Prompt-only]
- Cat identity: [visible type + preserved anchors]
- Gates: [plan / raster / visual — pass, fail, or not run]
- Quality: [pass, corrected once, or one precise limitation]
````

## Non-negotiable Outcome

The result must read in one glance: the same real cat, nine ordinary human situations, one gentle wrongness per situation, six small accents, and one cohesive flat sticker sheet. The cat-object mismatch creates the cuteness; complexity does not.
