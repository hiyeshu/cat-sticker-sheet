# scripts/
> L2 | 父级: ../CLAUDE.md

成员清单

CLAUDE.md: scripts 模块地图
validate_plan.py: 最小 sheet plan 的结构闸门——检查 9+6、2/4/3、编号、动作/主道具/单错位唯一性、呈现方式与文字一致性
compile_prompt.py: 猫咪身份与九个日常动作道具 JSON → backend-neutral Prompt；固定摄影拼贴、单步错位、9+6、纯色背景和单层白边
audit_sheet.py: 成图 raster 的机器闸门——画幅、背景纯度、连通域片数、出血、间隙、白边存在性与宽度一致性

设计决策：只把可稳定机器判定且直接影响画面的约束写进脚本。身份是否仍像源猫、动作是否一眼可读、每片是否只有一个轻微错位交给 quality-gate.md 的视觉枚举。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
