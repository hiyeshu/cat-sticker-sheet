# cat-sticker-sheet - 将单猫照片转为保留身份与视觉性格的写实荒诞猫头穿戴拼贴贴纸版
Agent Skills spec + Markdown/YAML/JSON contracts + Python 机器闸门 + built-in image generation

<directory>
skills/ - 可发现、可安装的 Skill 真源（1 子目录: cat-sticker-sheet，含 references/scripts/assets/evals）
output/ - 使用 Skill 生成并验收的项目内产物（1 子目录: cat-sticker-sheets，内含跨成图排除账本 ledger.json）
</directory>

<config>
CLAUDE.md - 项目宪法，维护仓库级边界与唯一真源位置
.gitignore - 排除 macOS 元数据、Python 字节码与本地虚拟环境，保持 Skill 仓库可安装且无运行噪声
</config>

法则：黄色成图是视觉机制锚点，不是猫咪身份、性格、具体道具、材质配对、文字或排版模板；目标猫图片始终是主体真源。每猫的外貌锚点与 visual_persona 驱动物件、表情和特殊材质。可判定契约由 scripts 机器闸门裁决，历史排除以 output/cat-sticker-sheets/ledger.json 为唯一账本。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
