---
name: cat-sticker-sheet
description: >-
  Turn one supplied cat photo or clear cat illustration into a finished 3:5
  photographic cut-paper collage sticker sheet with nine cat-head portraits,
  surreal wearables made from unexpected tactile materials, and six small
  accents. Use when the user asks for a cat sticker sheet, pet sticker pack,
  猫头贴纸, 猫咪表情贴纸, 荒诞穿戴猫, 特殊材质猫贴纸, 写实拼贴猫贴纸, or a
  prompt-only recipe for that look. Preserve visible breed/type and identity
  anchors, infer a distinct visual persona for this cat, and vary expressions
  without turning it into a generic cute mascot.
---

<!--
[INPUT]: 依赖一张清晰单猫主体图、assets/yellow-cat-collage-anchor.png、references/ 下的身份/视觉性格/材质变化规则、scripts/ 下的校验与编译器，以及内置 image_gen 能力
[OUTPUT]: 对外提供一张 3:5 写实荒诞猫头贴纸版、sheet plan JSON、编译产出的最终 Prompt、猫咪身份与视觉性格，以及两道闸门的验收结论
[POS]: cat-sticker-sheet 的请求路由与主执行流程，把可判定的表情/材质/版式契约交给机器闸门，把猫咪特有的荒诞穿戴交给变化引擎，阻止通用萌猫化和参考图照抄
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat Sticker Sheet

Turn one cat source into a cohesive family of photographic collage stickers: the same recognizable cat head appears once in each of nine persona-led surreal wearable concepts, while six tiny accents finish the page. Return one complete sheet plus the exact production prompt unless the user explicitly asks for prompt-only output.

## Hold The Product Contract

- Produce one flat 3:5 portrait raster, not separate PNGs, packaging, a photographed mockup, or a cutting-file claim.
- Default to exactly **9 main cat stickers + 6 accents**. Count cat depictions independently from accent pieces.
- Place exactly one head depiction of the source cat in each main sticker and exactly nine cat heads on the sheet. Keep the crop to face, ears, limited front paws, or minimal shoulders; never add a companion, mirrored second face, cloned head, kitten, human, mascot, or full-body scene.
- Preserve a recognition-oriented cat genome: user-provided breed or visible type, coat base, face mask or markings, ear silhouette, nose/muzzle, eye colors and their orientation, and distinctive marks. Keep the cat photographic; do not guess pedigree or promise biometric identity.
- Infer one **visual persona** from visible eyelid, gaze, mouth, ear and head-posture cues. Treat it as character direction, not a claim about real temperament. Define compatible and incompatible expressions so a cute, goofy, gentle, clever, aloof, sleepy, or other-looking cat keeps its own flavor.
- Make every familiar object physically engage the cat's head, ears or front paws. It may perch, wrap, frame, reshape, reveal, contain, or be operated; a loose prop pasted beside the face is a failure.
- Build absurdity from **familiar object × unexpected material × cat-specific fit × persona-consistent expression**. The material must show believable thickness, texture, folds, reflection, transparency, compression, or weight.
- Answer one question for every piece: **which normal position, role, or material expectation was displaced?** This is the `displaces` field and it is non-negotiable.
- Allocate the nine pieces across **nine distinct integration mechanisms in a bijection**; `nests` and `face_window` carry one slot each. Nine copies of the same construction are a failure even when the objects differ.
- Derive object, material, and expression choices partly from **this cat's own genome and visual persona** (`generative_cue`). At least three concepts must stop working if the cat were swapped; at least six must explain their `persona_fit`.
- Treat user examples such as fruit-peel headwear, towels, baseball, or coffee as seed directions only. Invent a new inventory for each run; never turn examples into a mandatory checklist.
- Keep the cross-output exclusion ledger on disk at `output/cat-sticker-sheets/ledger.json`. Deduplicate by semantic slot — object name, displaced expectation, and `mechanism × domain` — never by a hand-maintained blacklist of nouns.
- Use the photographic cut-paper collage grammar in `references/style-system.md`: realistic cat fur, tactile real-world materials, high-saturation retro color blocking, deadpan humor, slightly imperfect hand-cut contours, and restrained depth.
- Use one continuous white die-cut contour only. Never add a second colored outline, outer glow, layered rim, halo, or thick drop shadow.
- Default to a flat warm yellow background derived from the bundled anchor. Treat background color as a page-level variable: honor an explicit user color, but keep it one clean solid treatment with no scenery or texture.
- Allow zero to two short decorative English labels. Quote every permitted label exactly in the prompt, inspect its spelling, and prohibit all other text and logos.
- Use the built-in image-generation path by default. Do not silently switch to a CLI or external renderer.

## Route The Request

- **Generate — default:** inspect the cat, write its identity genome and visual persona, plan new cat-head concepts and material mismatches, compile the prompt, generate, inspect, correct once if needed, and return the selected sheet plus prompt.
- **Prompt-only:** when the user explicitly asks for a prompt without generation, return the complete bracket-free prompt, genome, and recipe. Do not claim an image was generated or inspected.
- **Missing input:** when the user says “这只猫” or equivalent but no usable image is available, ask for the cat image instead of inventing its appearance.
- **Multiple cats:** when more than one cat is prominent and the user has not named the hero, ask one focused question. Do not arbitrarily select one and never convert a single-cat request into duo or group stickers.
- **Independent-cat batch:** when the user supplies several separate single-cat images, make one sheet per cat. Give every sheet a different concept seed and maintain one exclusion ledger across the batch; never mix the cats on one page.

Assign each supplied image one role:

- **Subject source:** supplies the only cat that may appear; include it in generation.
- **Bundled style anchor:** `assets/yellow-cat-collage-anchor.png`; supplies collage medium, physical absurdity, border treatment, color energy, and loose page rhythm only.
- **User style reference:** may supply one additional medium, palette, or layout cue; never copy its cat, brand, text, watermark, inventory, or exact composition.
- **Supporting motif:** may supply one user-approved object or pattern, never another character.

The subject source always overrides every cat trait visible in a style reference.

## Load The References

- Read `references/style-system.md` for every request.
- Read `references/subject-genome.md` whenever an image is supplied.
- Read `references/shell-variation.md` before planning the nine cat-head concepts, special materials, expressions, and six accents.
- Read `references/prompt-compiler.md` and `references/sheet.schema.json` before writing a plan or returning a prompt.
- Read `references/quality-gate.md` before returning a generated result.

Three scripts carry the checks that must not depend on model tier:

- `scripts/validate_plan.py` — structural gate on the plan JSON; runs without vision, without a renderer.
- `scripts/compile_prompt.py` — plan JSON to renderer prompt; every fixed contract lives here as a constant.
- `scripts/audit_sheet.py` — raster gate: aspect, background solidity, piece count, bleed, gutter, single white contour.

Run them. Do not reimplement their judgements in prose, and do not report a pass they did not give.

## Generate The Sheet

1. **Inspect every input.** View each usable image before describing it. Record dimensions, role, subject count, robust cat anchors, source palette, visible objects, and every mark classified as intentional label, incidental text, signature, watermark, or UI. Do not guess unreadable traits.
2. **Write identity and visual persona.** Follow `references/subject-genome.md`. Record observed anchors separately from the inferred visual persona; write its expression language and avoid list; derive one `generative_cue` that drives object, material, or expression choice. If breed is user-provided, preserve its visible markers; otherwise write `unknown`. Lock heterochromia and asymmetric-marking orientation explicitly.
3. **Write the sheet plan JSON.** Follow `references/shell-variation.md` and `references/sheet.schema.json`: one seed, page system, nine mechanism-slotted cat-head pieces, at least five expressions, at least four material classes, at least two high-absurdity pieces, a filled `displaces`/`wearable_fit`/`persona_fit` for every piece, and six accents of which at least four are residues. Warm saturated yellow background by default; in a batch, vary page systems unless the user locks them.
4. **Gate the plan.** Run `python3 scripts/validate_plan.py plan.json --ledger output/cat-sticker-sheets/ledger.json`. On rejection, fix the plan — never bypass the gate, never argue with it in prose.
5. **Compile the prompt.** Run `python3 scripts/compile_prompt.py plan.json`. Do not hand-write renderer prompts; do not add brand names or negative lists to its output.
6. **Generate with the actual source.** Use built-in image generation. When every required image has a local path, pass the subject source first and the bundled yellow anchor second through `referenced_image_paths`; append any user style reference after them. When the subject exists only in conversation, use the smallest `num_last_images_to_include` that contains it and restate the complete written style grammar; never drop the subject merely to include the bundled anchor. Never use both image-input mechanisms.
7. **Gate the raster.** Run `python3 scripts/audit_sheet.py <image>` first; on pass, apply the vision gate in `references/quality-gate.md` — enumerate all fifteen rows, including identity anchors, expression, material behavior, and wearable fit. If either gate fails, regenerate once with one targeted correction while repeating the full cat identity, visual persona, counts, border, text, source-role, and anchor-boundary constraints.
8. **Persist and return.** For project-bound work, copy the selected output into `output/cat-sticker-sheets/` without overwriting an existing file, then append the plan to the ledger with `validate_plan.py --append`. For preview-only work, render it inline. Return the selected image, the plan JSON, the compiled prompt, and any remaining limitation stated precisely.

## Respect The Yellow Anchor Boundary

Borrow only:

- realistic cat-head cutouts physically integrated with oversized wearables or face frames;
- tactile material contrast and high-saturation retro color blocking;
- deadpan emotional tone, loose mixed-scale layout, one white contour, and sparse accent stickers.

Do not copy:

- the anchor cat's gray-mask/cream-coat traits when the user's cat differs;
- its objects, material pairings, phrases, and accent set — earlier inventory is seeded in `output/cat-sticker-sheets/ledger.json`, so `validate_plan.py` rejects it like any prior sheet; do not additionally maintain a prose blacklist;
- its exact sticker positions, palette mapping, yellow lighting, brands, logos, or composition.

Never mention or reproduce an external artist, collaboration, coffee brand, existing mascot, watermark, or signature. Describe and execute the visual mechanism in original terms.

## Renderer Boundary

- Keep the compiled prompt backend-neutral; use built-in image generation for execution.
- If built-in generation is unavailable, return the compiled prompt and state that no image was generated.
- If Python is unavailable, transcribe the compiler's field order by hand, self-check every validator judgement, and say the result is machine-unverified. If vision inspection is unavailable, downgrade to prompt-only honestly.
- Add a CLI route only after the user explicitly requests and authorizes that renderer and its requirements.

## Return This Shape

````markdown
**猫咪贴纸排版图**

![Cat sticker sheet](absolute-image-path-or-rendered-image)

**最终 Prompt**

```text
[the exact prompt used]
```

**说明**

- Mode: [Generate / Prompt-only]
- Cat identity: [breed or visible type + observed recognition anchors]
- Visual persona: [primary + expression language + avoid list + generative_cue]
- Plan: [sheet_id / seed / nine expression-object-material-mechanism combinations with their displaced expectation]
- Gates: [validate_plan ✓/✗, audit_sheet ✓/✗, vision enumeration ✓/✗ — or "not run" stated honestly]
- Quality: [pass, regenerated once, or one precise remaining limitation]
````

## Non-negotiable Outcome

A successful result reads instantly as one coherent cat-specific little world and one flat sticker sheet: nine genuinely different cat-head concepts whose expressions belong to this cat, unexpected materials that look physically real, convincing fit around face and ears, exactly one recognizable source cat head in each, six causal accents, one white border layer, lively color, no copied examples or prior inventory, no extra cats, and no mockup or 3D-toy drift.
