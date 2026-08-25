# cat-sticker-sheet - 将单猫照片转为日常人类道具轻错位并点缀图形化套壳肖像的复古摄影拼贴贴纸版
Agent Skills spec + Markdown/YAML references + built-in image generation + GD CLI fallback

<directory>
agents/ - Codex UI 元数据（1 文件: openai.yaml）
assets/ - 仅供维护者校准 Skill 视觉规则的资料（1 文件: yellow-cat-collage-anchor.png）
references/ - 身份、视觉样式、单步错位、轻量交付检查与 GD CLI 兜底（5 业务文件）
</directory>

<config>
SKILL.md - 仓库根入口与单 Skill 真源，可直接被 GitHub Skill 安装器发现
README.md - 面向仓库访问者的安装、调用与目录导航，不复制执行规则
CLAUDE.md - 项目宪法，维护根 Skill 与三个资源目录的边界
.gitignore - 排除 macOS 元数据与运行 output
</config>

法则：仓库根就是完整 Skill，禁止再包 `skills/<name>/`。固定输出为 3:5、9 主贴纸（2 大 + 4 中 + 3 小）、6 微贴纸、写实猫脸和单层白边；背景是每页变量，不设固定默认色或绝对纯色规则。内容以「熟悉人类道具 + 猫的可信互动 + 一个轻微错位」为主体，人类动作只作可选灵感；其中 2–3 片可用明显、图形化、接近超现实肖像的 face-in-cover 点缀，写实猫脸居中嵌入可识别物件外壳的干净开口，外壳遮住或替代身体。猫图只提供身份，不提供性格诊断；每片仍只讲一个笑点，禁止复杂奇幻世界。黄色图片仅供维护者校准摄影拼贴媒介、色彩能量、松散节奏与白边，不参与 Skill 运行，也不得传给任何渲染器。执行路径零脚本：内部写最终 Prompt，生成后只检查文件完整、主体正确和画面未灾难性缺失，不做逐项审美评分，也不自动发起第二次付费生成；对外只返回成图预览和可点击的绝对文件地址。运行环境只要暴露可调用的原生生图工具就必须使用它；只有完全没有生图工具时才允许 GD CLI 兜底。

[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
