<!--
[INPUT]: 依赖三张主体图、黄色锚点、三份实际 Prompt、选中 raster 与 quality-gate.md
[OUTPUT]: 对外提供本批次运行路径、猫咪基因、主题排除账本、校验结果与已知限制
[POS]: output/cat-sticker-sheets 的批次证据清单，连接可安装 Skill 真源与实际生成结果
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat sticker sheet run manifest

Run date: 2026-08-24

Skill source: ../../skills/cat-sticker-sheet/SKILL.md

Yellow anchor: ../../skills/cat-sticker-sheet/assets/yellow-cat-collage-anchor.png

Anchor SHA-256: c564aaad1a56dd51d4c4dabc160412304caaf5be3fe01ac5eb2dbbe1cdf273a9

## White short-hair

- Source: /var/folders/vm/56d7_00s6cj1h83b6jy4vc300000gn/T/codex-clipboard-7c37b089-9ac3-4019-b1ee-c0d0415f38fe.png
- Genome: creamy-white short coat, warm beige ear/forehead shading, pink nose, upright ears, viewer-left blue-gray eye, viewer-right deep green-gray/charcoal eye, calm alert attitude
- Concept: Tiny Indoor Weather
- Background: warm sunshine yellow
- Output: white-odd-eye-indoor-weather.png
- Prompt: white-odd-eye-indoor-weather.prompt.txt
- Inventory: 9 main + 6 accents
- Quality: cat count, genome, integration variety, spelling, single white edge, separation, and cross-output novelty pass
- Limitation: generated yellow field has mild tonal falloff and is visually solid rather than mathematically one RGB value

## Cream long-hair

- Source: /var/folders/vm/56d7_00s6cj1h83b6jy4vc300000gn/T/codex-clipboard-4216dd91-bd8e-4142-b564-2e9720e57779.png
- Genome: long cream-and-peach coat, white muzzle/chest, huge near-black eyes, pink nose, small soft ears, full tail, curious upward gaze
- Concept: Fluff Housekeeping Parade
- Background: saturated teal
- Output: cream-longhair-fluff-duty.png
- Prompt: cream-longhair-fluff-duty.prompt.txt
- Inventory: 9 main + 5 independently cuttable accents
- Quality: cat count, genome, imaginative fur integration, spelling, single white edge, separation, and first-sheet exclusion pass
- Limitation: the requested wooden thread-spool accent did not become an independent sixth accent after one targeted correction; the better 9+5 image is retained
- Limitation: generated teal field has mild tonal falloff and is visually solid rather than mathematically one RGB value

## Calico

- Source: /var/folders/vm/56d7_00s6cj1h83b6jy4vc300000gn/T/codex-clipboard-f84b75e4-e71d-4441-9c94-99792f53a820.png
- Genome: asymmetric orange/dark/white calico map, white muzzle/chest, green eyes, pink nose, pointed ears, signature viewer-left head tilt
- Concept: The Crooked Little Repair House
- Background: saturated raspberry coral
- Output: calico-crooked-repair.png
- Prompt: calico-crooked-repair.prompt.txt
- Inventory: 9 main + 6 accents
- Quality: cat count, asymmetric coat map, green eyes, head tilt, mechanism variety, spelling, single white edge, separation, and full cross-output exclusion pass
- Limitation: generated coral field has mild tonal falloff and is visually solid rather than mathematically one RGB value

## Cross-output exclusion ledger

| Sheet | Theme | Dominant field | Object language | Layout | Accent language |
| --- | --- | --- | --- | --- | --- |
| White short-hair | Tiny Indoor Weather | Sunshine yellow | pillow filling, weather dome, shower bonnet, file fan, hand-crank weather machine, hot-water warmth, watering cloud, powder puff, measuring-cup skirt | central hero with diagonal orbit | weather tag, bubbles, key, quilt patch, SOFT FORECAST, STAY IN |
| Cream long-hair | Fluff Housekeeping Parade | Teal | curtain tassel, hanger sweater, blind cord, sewing fringe, planter plume, ribbon tail, glasses lining, ironing cover, tail duster | two-corner S-shaped zigzag | ribbon bow, button cluster, tassel, FLUFF DUTY, BUSY LATER |
| Calico | Crooked Little Repair House | Raspberry coral | clock pendulum, bread-box lid, step-stool balance, wall switch, cookie jar, spice carousel, crooked apron, bookend bookmark, spiral trivet | asymmetrical vertical river | clock hands, hinge, blank recipe card, jar lid, TILT OK, I MEANT THAT |

No exact object-plus-integration pair, layout, phrase pair, accent quartet, or dominant field is reused across the three selected sheets.

## Skill verification

- skill-creator quick_validate.py: pass
- evals/evals.json parse: pass
- Template-placeholder scan: pass
- Skills CLI local discovery: one skill found, cat-sticker-sheet
