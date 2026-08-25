<!--
[INPUT]: 依赖用户猫咪主体图与用户确认的黄色猫咪拼贴锚点中可复用的视觉机制，不依赖锚点中的具体猫、道具、文字、品牌或排版
[OUTPUT]: 对外提供 Photographic Surreal Cat-head Sticker Sheet 的身份保真、视觉性格、特殊材质、猫头穿戴、色彩、背景、单层白边与反向约束
[POS]: references 的视觉身份真源，被主流程、Prompt 编译器与质量门共同消费，统一“真实猫 + 可信材质 + 不合理组合”的视觉语法
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Photographic Surreal Cat-head Sticker Sheet

中文名：写实荒诞猫头穿戴拼贴贴纸版

## Fixed System

- **Artifact:** one finished flat sticker-sheet image, never a photographed mockup or separate files.
- **Canvas:** default 3:5 portrait, full-frame background, loose mixed-scale collage.
- **Inventory:** exactly 9 main cat-head stickers plus 6 accent stickers by default.
- **Cat count:** each main piece contains one depiction of the source cat's head; accents contain no cat face or body. The full page therefore contains exactly nine cat heads.
- **Head-first crop:** use face, face-and-ears, face-and-front-paws, or a minimal head-and-shoulders crop. Do not drift into nine full-body scenes.
- **Cat identity:** keep the cat photographic and recognition-oriented. Preserve user-provided breed when known and all visible breed/type cues, real fur, natural eye surfaces, true coat relationships, ear shape, nose, muzzle, and defining marks. If breed is not supplied, never invent pedigree from appearance.
- **Visual persona:** derive one image-based character impression from eyelids, gaze, mouth, ears and head posture. Treat it as visual direction, not the animal's true personality. Vary expressions inside this grammar; never turn every cat into the same generic cute mascot.
- **Wearable mechanism:** make an oversized familiar object perch on, wrap, frame, reshape, reveal, contain or be worked by the head, ears or front paws. Fit the opening and load path deliberately around the skull and ears. A loose prop pasted beside the face does not count.
- **Absurdity:** combine a familiar object with an unexpected but physically legible material and a persona-consistent deadpan expression. Every piece states what normal position, role or material expectation it displaces. Random prop accumulation is not a joke.
- **Integration variety:** use the nine mechanisms in `shell-variation.md`; `nests` and `face_window` carry one slot each. `scripts/validate_plan.py` enforces mechanism, expression, material-class, domain and absurdity coverage.
- **Material credibility:** render tactile real-world thickness and behavior. Fabric compresses and folds; translucent matter has depth and refraction; reflective matter carries environmental highlights; brittle shells show openings and support; crinkled packaging keeps creases. A flat recolor is not a material change.
- **Collage medium:** use high-quality photographic cut-paper collage, slightly imperfect hand-cut outer contours, and restrained internal photographic depth. Keep the real cat face sharper than the surrounding construction.
- **Tone:** cute, anthropomorphic and mildly absurd, with dry or deadpan restraint. Let the cat's own visual persona survive; the object-material mismatch carries most of the comedy.
- **Color:** use saturated retro color blocking with cream neutrals and two to four lively hues. Avoid muddy gray palettes.
- **Background:** use one clean solid field. Default to saturated warm yellow near `#FFC21A`; honor a user-requested alternative color. No scenery, paper grain, pattern, gradient, vignette, center glow, or multiple color zones.
- **Border:** give every piece exactly one continuous white die-cut contour in one visually consistent absolute width across the page, about 2% of canvas width. White is the only outline color. No second rim, colored stroke, halo, glow, layered contour, or thick drop shadow.
- **Separation:** keep every piece fully inside the canvas with visible background gutter. Borders never touch, overlap, or merge.
- **Text:** permit zero to two short uppercase deadpan labels as accent stickers. Quote them verbatim and prohibit all other words, letters, brands, watermarks, and signatures.

## Variable System

- Breed/type evidence, recognition anchors, visual persona, expression language, and forbidden expressions vary per cat.
- Inspiration domain spans food, drink, bath, sport, fashion, packaging, desk, home, travel, nature, industrial, and toy contexts; user examples are seeds, never mandatory inventory.
- Material class spans food-derived, textile, paper, packaging, transparent, reflective, rigid, organic, and mixed constructions; every chosen material also needs a visible behavior.
- Cat crop stays head-led: face, face-and-ears, face-and-paws, or minimal head-and-shoulders.
- Layout rhythm may use a loose three-column stack, two-hero top anchor, or diagonal mixed-scale constellation.
- Concept seed combines one cat cue, one persona cue, two material cues, and one absurdity rule; never render the internal theme title as text unless approved.
- Text accents: zero, one, or two; derive them from the user's mood and never copy the bundled anchor's phrases.

## Yellow Anchor Role

Use `../assets/yellow-cat-collage-anchor.png` as a style reference only. Borrow its photographic collage medium, tactile contrast, saturated color energy, sparse accents, white-border logic, loose page rhythm, and physically legible absurdity. The written system overrides every visible detail in the anchor.

Never borrow its cat traits, exact objects, material-object pairings, phrases, logos, palette placement, sticker positions, lighting falloff, or composition. The target cat source is always the sole authority for cat appearance and visual persona.

## Anti-style

Avoid generic cute-cat averaging, invented breeds, nine identical expressions, unrelated personality shifts, full-body scene drift, hand-drawn line art, watercolor, crayon, plush-doll redesign, fuzzy mascot anatomy, clay, glossy 3D toys, vector-perfect icons, anime eyes, fashion illustration, portrait painting, physically flat “special” materials, impossible ear occlusion, airbrush gradients, dramatic studio lighting, deep cast shadows, double outlines, colored outer rims, sticker mockups, packaging, hands holding the sheet, hard equal-cell grids, full-bleed scenes, overlapping pieces, cropped borders, random slogans, copied anchor props, copied previous-sheet objects, repeated face-in-a-hole templates, generic accent reuse, copied brand elements, extra cats, duplicated faces, or unrelated companions.
