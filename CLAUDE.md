# cat-sticker-sheet - 将单猫照片转为日常人类道具轻错位的复古摄影拼贴贴纸版
Agent Skills spec + Markdown/YAML/JSON contracts + Python 机器闸门 + built-in image generation

<directory>
agents/ - Codex UI 元数据（1 文件: openai.yaml）
assets/ - 生成时使用的次级视觉媒介锚点（1 文件: yellow-cat-collage-anchor.png）
references/ - 身份、视觉样式、单步错位、Schema 与质量门（5 业务文件）
scripts/ - 计划校验、Prompt 编译与成图审计机器闸门（3 Python 文件）
</directory>

<config>
SKILL.md - 仓库根入口与单 Skill 真源，可直接被 GitHub Skill 安装器发现
README.md - 面向仓库访问者的安装、调用与目录导航，不复制执行规则
CLAUDE.md - 项目宪法，维护根 Skill 与四个资源目录的边界
.gitignore - 排除 macOS 元数据、Python 字节码、本地虚拟环境与运行 output
</config>

法则：仓库根就是完整 Skill，禁止再包 `skills/<name>/`。固定输出为 3:5、9 主贴纸（2 大 + 4 中 + 3 小）、6 微贴纸、写实猫脸、纯色背景和单层白边。内容只用「普通人类动作 + 熟悉主道具 + 猫的可信互动 + 一个轻微错位」；猫图只提供身份，不提供性格诊断。黄色图片只提供摄影拼贴媒介、色彩能量、松散节奏与白边，不提供猫咪身份、具体道具、文字或构图。可判定契约由 scripts 裁决。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
