<!--
[INPUT]: 依赖实际生成的图片与用户指定的猫咪主体
[OUTPUT]: 对外提供文件完整、主体正确、画面未灾难性缺失三项最低交付检查，不触发自动重生成
[POS]: references 的轻量交付检查，只拦截坏文件、错主体和明显残缺，不评价审美或逐项核对 Prompt
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# Minimal Delivery Check

The prompt defines the target. This check only prevents a broken artifact from being presented as a successful delivery.

Confirm only three things:

1. **File integrity:** the downloaded result decodes as a non-empty raster with valid dimensions.
2. **Hero subject:** the image is visibly led by the intended source cat, not a different species, unrelated subject, or accidental multi-cat scene.
3. **Usable frame:** the result is not blank, an error placeholder, or so severely clipped/corrupted that the central sticker sheet is missing.

Do not count stickers, enumerate concepts, score identity anchors, measure scale tiers, grade face-in-cover usage, police minor text artifacts, compare backgrounds, or reject normal renderer variation. Do not trigger a second paid generation from this check.

If one catastrophic check fails, still return an openable generated image with one concise limitation. Run another generation only when the user explicitly asks. If no image exists or the file cannot decode, report the generation failure without substituting the internal prompt.
