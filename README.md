<!--
[INPUT]: 依赖根目录 SKILL.md 的产品契约与 GitHub 单 Skill 安装路径
[OUTPUT]: 对仓库访问者提供用途、安装、调用与目录结构的最小说明
[POS]: cat-sticker-sheet 的人类入口，只做导航，不复制 references/ 中的运行规则
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Cat Sticker Sheet

把一张猫咪照片变成一张复古流行、低保真摄影拼贴风格的荒诞猫脸外壳贴纸版。

它会保留猫咪可见的品种/类型、毛色、花纹、脸型、耳朵与眼睛特征，并根据这只猫呈现出的视觉性格安排表情。每张写实猫脸都嵌在夸张 wearable cover shell 的干净开口中央，外壳采用意外但可信的特殊材质。最终生成一张 3:5、2 大 + 4 中 + 3 小主贴纸、6 枚微贴纸、统一单层白色模切描边的贴纸版。

## 安装

```bash
npx skills add https://github.com/hiyeshu/cat-sticker-sheet -g -a codex --skill cat-sticker-sheet -y
```

## 使用

向 Codex 附上一张清晰的单猫照片，然后调用：

```text
Use $cat-sticker-sheet to turn this cat into a surreal cat-head sticker sheet.
```

也可以直接用中文描述想要的方向，例如：

```text
用 $cat-sticker-sheet 保留这只猫的品种和脸部特征，生成一组可爱、拟人、略带荒诞的猫头贴纸。穿戴物使用特别的真实材质，统一白色描边。
```

西瓜皮、浴巾、棒球、咖啡等只会被视为灵感示例，不是固定生成清单。

## 设计原则

- 同一只猫，而不是通用萌猫模板。
- 表情服从这只猫的视觉性格。
- 固定形态是“写实猫脸居中 × 夸张外壳遮身”，不会漂移成九个全身场景。
- 荒诞来自“熟悉物件 × 意外材质 × 可信开口与受力”。
- 风格参考只提供媒介与节奏，不提供猫咪身份、具体道具或排版。
- 生成结果与运行账本写入调用项目，不写回 Skill 安装目录。

## 目录

```text
SKILL.md     Skill 入口与执行流程
agents/      Codex UI 元数据
assets/      原创视觉风格锚点
references/  身份、性格、材质、Schema 与质量规则
scripts/     计划校验、Prompt 编译与成图审计
```
