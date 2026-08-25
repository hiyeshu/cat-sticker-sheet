# scripts/
> L2 | 父级: ../CLAUDE.md

成员清单

CLAUDE.md: scripts 模块地图
validate_plan.py: sheet plan JSON 的结构闸门——机制双射、荒诞落点、尺度/灵感领域/材质类别/表情/荒诞度配额、装饰余波、对 ledger.json 的语义档位去重与 --append 记账
compile_prompt.py: 身份/visual_persona/特殊材质 sheet plan JSON → backend-neutral 渲染器 Prompt；猫头 9+6、材质可信、视觉语法与反向约束作为常量写死于此，输出中禁止品牌名
audit_sheet.py: 成图 raster 的机器闸门——画幅比、背景纯度、连通域片数（外部可达性过滤）、出血、最小间隙、白边存在性与宽度一致性（双层边缘检测）

设计决策: 三个脚本承载「可判定」的检查，使其与模型层次无关；身份是否仍像这只猫、表情是否属于其视觉性格、材质是否可信等「需要眼睛」的判断留给 quality-gate.md。校验失败的正确响应是修计划，不是绕闸门。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
