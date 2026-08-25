<!--
[INPUT]: 依赖 sheet.schema.json 的字段契约、subject-genome.md 的身份与视觉性格，以及 shell-variation.md 的 face-in-cover 外壳、表情和特殊材质分配结果
[OUTPUT]: 对外提供「变量写 JSON、常量写编译器」的分层规则，以及 scripts/compile_prompt.py 的调用方式与 Prompt-only 交付要求
[POS]: references 的编译层，取代旧的人工填空散文模板；被 Generate 与 Prompt-only 两条路径共同消费
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Prompt 编译

**不要手写渲染器 prompt。**写一份 sheet plan JSON，交给编译器。

## 四层分离

散文 prompt 的病根，是把四类完全不同的东西写成同一种语气，于是每张都要重打一遍，每张都会漂移一点。

| 层 | 内容 | 归属 | 变不变 |
|---|---|---|---|
| 产物契约 | 3:5、15 片、单层白边 2%、不重叠不出血、反 3D／水彩／plush | `scripts/compile_prompt.py` 常量 | 永不变 |
| 页面变量 | 背景色、调色板、layout、mood、文字 | JSON `page` | 每页变 |
| 主体变量 | 品种/类型证据、识别锚点、visual_persona、generative_cue | JSON `subject` | 每猫变 |
| 内容变量 | 九个 cover shell 的表情、物件、特殊材质、开口受力与荒诞落点，六枚微贴纸 | JSON `pieces` / `accents` | **每页必须全变** |

排除项不进 plan JSON——那是 `anchor-exclusions.json`、项目运行 ledger 与校验器的职责。plan JSON 只描述这一页**是**什么。

> **正面描述归 JSON，负面约束归编译器和校验器，IP 边界只留在 SKILL.md。**

## 外部专名绝不进渲染器 prompt

不要在送给渲染器的文本里点名任何外部项目、合作、创作者或它们的具体道具。**告诉渲染器「别画 X」的同时，你已经把 X 放进了它的条件里**；图像模型对否定式的遵从本来就弱，这类句子会反向拉高漂移概率。列举对方的具体造型清单尤其危险。

正确做法：原创边界只作为规则写在 SKILL.md，供模型在**选择内容时**遵守；编译产物里不出现任何外部专名。

## 写 sheet plan

字段契约见 `sheet.schema.json`。承重字段四组：

- `subject.visual_persona` — 这只猫在照片里呈现什么角色气质、用什么表情语法、哪些表情会把它画成另一只猫。
- `subject.generative_cue` — 这只猫的哪个特征驱动物件、材质或表情。缺失则整页换只猫也成立。
- `pieces[].displaces` — 打破了哪一种正常位置、角色或材料预期。填不出来这片作废。
- `pieces[].material_behavior` / `wearable_fit` / `persona_fit` — 材质如何可见、物件如何顺着猫头受力、这张为何只属于这只猫。

`pieces[].mechanism` 九片九种、双射，但全部必须回到「写实猫脸居中嵌入夸张外壳」的可见骨架；至少五种表情、四类材质、两片高荒诞度、六个灵感领域；`accents` 至少四枚声明 `residue_of`。这些由校验器裁决，不靠自觉。

## 执行顺序

```bash
# 1. 结构闸门。不通过就不许编译，更不许出图。
python3 <skill-dir>/scripts/validate_plan.py <plan.json> --ledger <active-project>/output/cat-sticker-sheets/ledger.json

# 2. 编译成 backend-neutral prompt
python3 <skill-dir>/scripts/compile_prompt.py <plan.json> -o <prompt.txt>

# 3. 出图、成图审计（见 quality-gate.md）、通过后记账
python3 <skill-dir>/scripts/validate_plan.py <plan.json> --ledger <active-project>/output/cat-sticker-sheets/ledger.json --append
```

调用项目的 ledger 不存在时无需预建；校验器仍会加载 Skill 内只读的 `references/anchor-exclusions.json`，首次 `--append` 时再在调用项目创建运行账本。

校验器拒收时，**修计划，不要绕过校验器**。拒收信息已经指明是哪一片、哪个字段。

## Prompt-only 模式

用户明确只要 prompt 时：

- 照常写 JSON、照常跑校验器——**它是纯文本检查，不需要出图**；
- 返回编译产物全文、JSON 计划与视觉基因；
- 明确声明未生成、未做视觉验收；
- 不得出现未替换的占位符、`various funny props` 这类含糊表达，或任何外部专名。

若运行环境没有 Python，可按 `compile_prompt.py` 的字段顺序人工誊写，但仍须逐条自查校验器的判据，并在交付时说明「未经机器校验」。
