# cat-sticker-sheet/
> L2 | 父级: ../CLAUDE.md

成员清单

CLAUDE.md: Skill 模块地图，维护入口、参考、脚本、资产、评测与 UI 元数据边界
SKILL.md: 请求路由和主执行流程——身份/视觉性格提取、猫头穿戴与特殊材质 sheet plan JSON、两道机器闸门（validate_plan / audit_sheet）、视觉枚举质检与最终交付契约
agents/: Codex UI 元数据，成员见 agents/CLAUDE.md
assets/: 原创黄色风格锚点（其九件物件由 output/cat-sticker-sheets/ledger.json 首条记录承担排除），成员见 assets/CLAUDE.md
evals/: 可复用行为评测，成员见 evals/CLAUDE.md
references/: 猫头视觉系统、猫咪身份与 visual_persona、材质/表情槽位分配、编译分层与质量门，成员见 references/CLAUDE.md
scripts/: 计划校验、Prompt 编译与成图审计三件套，承载机制/材质/表情/版式等与模型层次无关的可判定检查，成员见 scripts/CLAUDE.md

架构决策: 可判定契约（计数、几何、描边、去重、材质/表情/荒诞配额）交给 scripts 的机器闸门；不可判定的品味（身份一致性、性格是否贴猫、材质是否可信）交给强制枚举的视觉闸门。displaces 陈述被打破的正常预期，wearable_fit 与 persona_fit 分别锁定物理受力和角色归属。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
