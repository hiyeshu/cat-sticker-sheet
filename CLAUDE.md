# cat-sticker-sheet - 将单猫照片转为保留身份与视觉性格的写实荒诞猫头穿戴拼贴贴纸版
Agent Skills spec + Markdown/YAML/JSON contracts + Python 机器闸门 + built-in image generation

<directory>
agents/ - Codex UI 元数据（1 文件: openai.yaml）
assets/ - 生成时使用的原创视觉锚点（1 文件: yellow-cat-collage-anchor.png）
references/ - 身份、性格、材质、Prompt、Schema、质量门与锚点排除种子（8 文件）
scripts/ - 计划校验、Prompt 编译与成图审计机器闸门（3 Python 文件）
</directory>

<config>
SKILL.md - 仓库根入口与单 Skill 真源，可直接被 GitHub Skill 安装器发现
CLAUDE.md - 项目宪法，维护根 Skill 与四个资源目录的边界
.gitignore - 排除 macOS 元数据、Python 字节码、本地虚拟环境与运行 output，保持 Skill 包只含可安装真源
</config>

法则：仓库根就是完整 Skill，禁止再包 `skills/<name>/`。黄色成图是视觉机制锚点，不是猫咪身份、性格、具体道具、材质配对、文字或排版模板；目标猫图片始终是主体真源。可判定契约由 scripts 机器闸门裁决；仓库只保存 anchor-exclusions.json，运行历史写入调用项目的 output/cat-sticker-sheets/ledger.json，不回流 Skill 包。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
