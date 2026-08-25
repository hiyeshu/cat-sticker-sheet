#!/usr/bin/env python3
# [INPUT]: 依赖一张已生成的贴纸版 raster 与 style-system.md 的画幅、纯色背景、单层白边与间隙契约
# [OUTPUT]: 对外提供不依赖视觉模型的成图硬闸门：画幅比、背景纯度、连通域片数、出血、间隙、白边存在性与宽度一致性
# [POS]: scripts 的成图审计器，承担 quality-gate.md 前段的可判定检查，把计数与描边从 VLM 自评中剥离
# [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""用法:
    python3 scripts/audit_sheet.py sheet.png [--pieces 15]

只判定可判定的：数量、几何、边界。身份、动作可读性与单步错位仍归视觉质检。
退出码 0 = 通过，1 = 拒收。
"""
import argparse, sys

try:
    import numpy as np
    from PIL import Image
    from scipy import ndimage
except ImportError as e:
    print(f"缺少依赖: {e}. 需要 numpy / pillow / scipy", file=sys.stderr)
    sys.exit(2)

ASPECT = 3 / 5
ASPECT_TOL = 0.01
BG_TOL = 60          # 与背景色的 L1 距离阈值
SPECK = 0.0008       # 小于画布此比例的连通块视为噪点
WHITE_MIN = 200      # 白边判定：三通道最小值
WHITE_SPREAD = 45    # 白边判定：三通道极差上限
AA_SKIP = 1          # 轮廓最外一圈是抗锯齿过渡，量白边时跳过


def _components(a, bg, W, H):
    """只把从画布边缘可达的背景算作背景。

    编织篮的孔隙、条纹灯罩的亮条、与背景同色的挂牌，颜色都落在背景容差里；
    若不做外部可达性过滤，它们会被当成背景，让片数与白边测量全部失真。
    """
    raw = np.abs(a - bg).sum(axis=2) < BG_TOL
    seed = np.zeros_like(raw)
    seed[0, :] = seed[-1, :] = seed[:, 0] = seed[:, -1] = True
    bgmask = ndimage.binary_propagation(seed & raw, mask=raw)
    lbl, n = ndimage.label(~bgmask)
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s > W * H * SPECK]
    return bgmask, lbl, keep, sizes


def _white(a):
    return (a.min(axis=2) > WHITE_MIN) & ((a.max(axis=2) - a.min(axis=2)) < WHITE_SPREAD)


def audit(path, expect=15):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(int)
    err, warn, info = [], [], []

    # 1 画幅
    ar = W / H
    info.append(f"画幅 {W}x{H} = {ar:.4f}（3:5 = {ASPECT:.4f}）")
    if abs(ar - ASPECT) > ASPECT_TOL:
        err.append(f"画幅比 {ar:.4f} 偏离 3:5 超过 {ASPECT_TOL}")

    # 2 背景纯度
    corners = [tuple(a[2, 2]), tuple(a[2, W - 3]), tuple(a[H - 3, 2]), tuple(a[H - 3, W - 3])]
    bg = np.array(max(set(corners), key=corners.count))
    bgmask, lbl, keep, sizes = _components(a, bg, W, H)
    cov = bgmask.mean()
    std = a[bgmask].std(axis=0).max() if bgmask.any() else 0
    info.append(f"背景 rgb{tuple(int(x) for x in bg)}，覆盖 {cov*100:.1f}%，通道标准差 {std:.1f}")
    if cov < 0.15:
        err.append(f"背景仅覆盖 {cov*100:.1f}%，间隙不足或存在满版元素")
    if std > 12:
        err.append(f"背景通道标准差 {std:.1f} 偏高 → 存在渐变、暗角、纹理或中心辉光")
    elif std > 6:
        warn.append(f"背景通道标准差 {std:.1f} → 轻微色调不均，交付时如实说明，勿称『数学纯色』")

    # 3 片数
    info.append(f"连通域片数 {len(keep)}")
    if len(keep) != expect:
        err.append(f"数出 {len(keep)} 片，应为 {expect} 片"
                   + ("（少于预期 → 大概率有两片轮廓相接被并成一块）" if len(keep) < expect else ""))

    boxes = []
    for i in keep:
        sl = ndimage.find_objects(lbl == i)[0]
        boxes.append((int(sizes[i - 1]), sl[1].start, sl[0].start,
                      sl[1].stop - sl[1].start, sl[0].stop - sl[0].start, i))
    boxes.sort(reverse=True)

    # 4 出血
    bleed = [b for b in boxes
             if b[2] == 0 or b[1] == 0 or b[1] + b[3] >= W or b[2] + b[4] >= H]
    if bleed:
        err.append(f"{len(bleed)} 片触碰画布边缘: " + ", ".join(f"bbox(x={b[1]},y={b[2]})" for b in bleed))

    # 5 间隙：逐步膨胀，看片数在多小的半径就开始塌陷
    pieces = np.isin(lbl, keep)
    gutter = None
    for r in range(1, 13):
        st = ndimage.generate_binary_structure(2, 2)
        grown = ndimage.binary_dilation(pieces, structure=st, iterations=r)
        _, n2 = ndimage.label(grown)
        if n2 < len(keep):
            gutter = 2 * r
            break
    if gutter is None:
        info.append("最小间隙 > 24px")
    else:
        info.append(f"最小间隙 ≈ {gutter}px")
        if gutter <= 4:
            err.append(f"最小间隙仅 ≈{gutter}px → 两片轮廓几乎相接，违反可见间隙契约")
        elif gutter <= 10:
            warn.append(f"最小间隙 ≈{gutter}px 偏紧")

    # 6 白边存在性与宽度一致性
    white = _white(a)
    dist = ndimage.distance_transform_edt(~bgmask)
    widths = []
    for area, x, y, w, h, i in boxes:
        m = lbl == i
        t = 0
        # d=1 是抗锯齿过渡环，必然掺背景色，从 d=2 起量
        for d in range(AA_SKIP + 1, 40):
            ring = m & (dist > d - 1) & (dist <= d)
            if ring.sum() < 30:
                break
            if white[ring].mean() >= 0.70:
                t = d
            else:
                break
        widths.append(t)
        if t == 0:
            err.append(f"bbox(x={x},y={y}) 外缘不是白色 → 缺少白色模切轮廓或被彩色描边覆盖")
    if widths and min(widths) > 0:
        med = float(np.median(widths))
        spec = W * 0.02
        info.append(f"白边宽度中位数 {med:.0f}px，范围 {min(widths)}–{max(widths)}px"
                    f"（画布宽 {W}，契约 2% ≈ {spec:.0f}px）")
        if med < spec * 0.6:
            warn.append(f"白边中位数 {med:.0f}px 明显细于契约的 {spec:.0f}px")
        thin = [(b, t) for b, t in zip(boxes, widths) if t < med * 0.6]
        fat = [(b, t) for b, t in zip(boxes, widths) if t > med * 1.6]
        for b, t in thin:
            err.append(f"bbox(x={b[1]},y={b[2]}) 白边仅 {t}px，其余为 {med:.0f}px"
                       f" → 疑似彩色底板外包一圈细白边的双层边缘，非单层模切轮廓")
        for b, t in fat:
            err.append(f"bbox(x={b[1]},y={b[2]}) 白边 {t}px，其余为 {med:.0f}px → 宽度不成一套系统")

    return err, warn, info, boxes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--pieces", type=int, default=15)
    ap.add_argument("--boxes", action="store_true", help="打印每片的 bbox，便于定位问题片")
    a = ap.parse_args()

    err, warn, info, boxes = audit(a.image, a.pieces)
    print(f"== {a.image.split('/')[-1]} ==")
    for x in info:
        print("  ·", x)
    if a.boxes:
        for area, x, y, w, h, _ in boxes:
            print(f"    area={area:7d}  x={x:4d} y={y:4d} w={w:4d} h={h:4d}")
    for x in err:
        print("  ✗", x)
    for x in warn:
        print("  !", x)
    print(f"\n{'拒收' if err else '通过'}：{len(err)} 项硬伤 / {len(warn)} 项提示")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
