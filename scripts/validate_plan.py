#!/usr/bin/env python3
# [INPUT]: 依赖 references/sheet.schema.json 的字段契约、references/anchor-exclusions.json 的锚点排除种子与可选调用项目 ledger
# [OUTPUT]: 对外提供出图前的结构硬闸门（机制双射、荒诞落点、尺度/领域/材质/表情配额、装饰余波、跨成图去重）与项目 ledger 追加
# [POS]: scripts 的计划校验器，把 shell-variation.md 中可判定的猫头变化与材质错位规则变成机器拒收条件，被 SKILL.md 第 4 步调用
# [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""用法:
    python3 scripts/validate_plan.py plan.json [--ledger PATH] [--append]
不需要模型，不需要看图。JSON 进，通过/拒收 出。退出码 0 = 通过，1 = 拒收。
"""
import argparse, collections, json, os, sys

MECHS = ["becomes_part", "replaces_silhouette", "wraps", "wears", "operates",
         "spills_from", "peeks_through", "nests", "face_window"]
SCALE_QUOTA = {"hero": 2, "medium": 4, "small": 3}
MIN_DOMAINS = 6
MIN_MATERIAL_CLASSES = 4
MIN_EXPRESSIONS = 5
MIN_HIGH_ABSURDITY = 2
MIN_NONLOW_ABSURDITY = 5
LEDGER_PAIR_WINDOW = 3          # (mechanism, domain) 档位在最近 N 页内不得复用
EMPTY_DISPLACES = {"", "-", "无", "内部", "空腔", "内腔", "里面", "中空",
                   "nothing", "none", "interior", "inside", "empty", "empty space", "n/a"}


# ---------------------------------------------------------------- schema 层
def check_schema(plan, schema_path):
    """有 jsonschema 就做完整校验，没有就退回到必填键的最小检查。"""
    try:
        import jsonschema
    except ImportError:
        errs = []
        for k in ("sheet_id", "seed", "subject", "page", "pieces", "accents"):
            if k not in plan:
                errs.append(f"缺少顶层字段: {k}")
        return errs, True
    try:
        jsonschema.validate(plan, json.load(open(schema_path, encoding="utf-8")))
        return [], False
    except jsonschema.ValidationError as e:
        return [f"schema: {'/'.join(str(x) for x in e.path)} → {e.message}"], False


# ---------------------------------------------------------------- 结构层
def check_structure(plan):
    err, warn = [], []
    P, A, freeform = plan["pieces"], plan["accents"], plan.get("freeform", False)

    if len(P) != 9:
        err.append(f"主贴纸 {len(P)} 片，应为 9")
    if len(A) != 6:
        err.append(f"装饰 {len(A)} 枚，应为 6")

    # 一条规则替代四条：九片九机制，双射
    ms = [p["mechanism"] for p in P]
    if freeform:
        if len(set(ms)) < 5:
            err.append(f"freeform 下仍需 ≥5 种机制，当前 {len(set(ms))} 种")
        if ms.count("face_window") > 1:
            err.append(f"face_window ×{ms.count('face_window')}，全页配额为 1")
        if ms.count("nests") > 2:
            err.append(f"nests ×{ms.count('nests')}，freeform 下上限为 2")
    else:
        for m, c in sorted(collections.Counter(ms).items()):
            if c > 1:
                err.append(f"机制重复 ×{c}: {m}")
        missing = [m for m in MECHS if m not in ms]
        if missing:
            err.append(f"未使用的机制: {', '.join(missing)}")

    # 荒诞必须有可陈述的落点：位置、角色或常规材质预期至少打破一个
    seen_disp = {}
    for p in P:
        d = p["displaces"].strip()
        if d.lower() in EMPTY_DISPLACES:
            err.append(f"#{p['n']} {p['object']}: displaces 为空 → 没说清打破了哪种正常预期，作废")
        elif d in seen_disp:
            err.append(f"#{p['n']} 与 #{seen_disp[d]} 顶替了同一个位置「{d}」")
        else:
            seen_disp[d] = p["n"]

    # 配额（freeform 放开尺度，不放开跨领域、材质、表情与荒诞度）
    if not freeform:
        sc = collections.Counter(p["scale"] for p in P)
        if {k: sc.get(k, 0) for k in SCALE_QUOTA} != SCALE_QUOTA:
            err.append(f"尺度配额 {dict(sc)}，应为 hero2 / medium4 / small3")

    dn = len({p["domain"] for p in P})
    if dn < MIN_DOMAINS:
        err.append(f"灵感领域仅 {dn} 种，应 ≥{MIN_DOMAINS}")

    material_classes = len({p["material_class"] for p in P})
    if material_classes < MIN_MATERIAL_CLASSES:
        err.append(f"材质类别仅 {material_classes} 种，应 ≥{MIN_MATERIAL_CLASSES}")

    expressions = len({p["expression"] for p in P})
    if expressions < MIN_EXPRESSIONS:
        err.append(f"表情仅 {expressions} 种，应 ≥{MIN_EXPRESSIONS}，不能给不同贴纸套同一张脸")

    absurdity = collections.Counter(p["absurdity"] for p in P)
    if absurdity.get("high", 0) < MIN_HIGH_ABSURDITY:
        err.append(f"high 荒诞度仅 {absurdity.get('high', 0)} 片，应 ≥{MIN_HIGH_ABSURDITY}")
    if absurdity.get("medium", 0) + absurdity.get("high", 0) < MIN_NONLOW_ABSURDITY:
        err.append(f"中高荒诞度共 {absurdity.get('medium', 0) + absurdity.get('high', 0)} 片，应 ≥{MIN_NONLOW_ABSURDITY}")

    for c, n in collections.Counter(p["color"] for p in P).items():
        if n > 3:
            warn.append(f"主色「{c}」出现 {n} 次，建议 ≤3")
    for m, n in collections.Counter(p["material"] for p in P).items():
        if n > 2:
            warn.append(f"材质「{m}」出现 {n} 次，建议 ≤2")

    if len({p["n"] for p in P}) != len(P):
        err.append("pieces.n 存在重复编号")

    # 装饰 = 主贴纸的因果余波
    res = [a for a in A if "residue_of" in a]
    txt = [a for a in A if "text" in a]
    if len(res) < 4:
        err.append(f"仅 {len(res)} 枚装饰声明了 residue_of，应 ≥4（装饰必须是某片的余波，不是主题的同义词）")
    if len({a["residue_of"] for a in res}) != len(res):
        err.append("多枚装饰指向同一片主贴纸，应各自来源不同")
    valid_n = {p["n"] for p in P}
    for a in res:
        if a["residue_of"] not in valid_n:
            err.append(f"装饰 {a['id']} 的 residue_of={a['residue_of']} 不存在")
    for a in A:
        if "text" not in a and "motif" not in a:
            err.append(f"装饰 {a['id']} 既无 motif 也无 text")
    if len(txt) > 2:
        err.append(f"文字装饰 {len(txt)} 枚，应 ≤2")
    if sorted(a.get("text", "") for a in txt) != sorted(plan["page"]["text"]):
        err.append(f"装饰文字 {[a.get('text') for a in txt]} 与 page.text {plan['page']['text']} 不一致")

    return err, warn


# ---------------------------------------------------------------- 跨成图层
def check_ledger(plan, ledger):
    """语义档位去重，不做词面黑名单——词面挡不住『沙拉甩干器 vs 滤水篮』。"""
    err, warn = [], []
    if not ledger:
        return err, warn
    P = plan["pieces"]
    mine = plan["sheet_id"]
    past = [e for e in ledger if e.get("sheet_id") != mine]

    ever_obj = {o: e["sheet_id"] for e in past for o in e.get("objects", [])}
    ever_disp = {d: e["sheet_id"] for e in past for d in e.get("displaces", [])}
    recent = {tuple(pair): e["sheet_id"]
              for e in past[-LEDGER_PAIR_WINDOW:] for pair in e.get("slots", [])}

    for p in P:
        if p["object"] in ever_obj:
            err.append(f"#{p['n']}「{p['object']}」与 {ever_obj[p['object']]} 完全同名")
        if p["displaces"] in ever_disp:
            err.append(f"#{p['n']} 顶替位置「{p['displaces']}」已用于 {ever_disp[p['displaces']]}")
        key = (p["mechanism"], p["domain"])
        if key in recent:
            err.append(f"#{p['n']} 档位 {key[0]}×{key[1]} 与近 {LEDGER_PAIR_WINDOW} 页内的 {recent[key]} 撞档")

    if past:
        prev = past[-1]
        if prev.get("background") == plan["page"]["background"]:
            warn.append(f"背景色与上一页 {prev['sheet_id']} 相同")
        if prev.get("layout") == plan["page"]["layout"]:
            warn.append(f"layout 与上一页 {prev['sheet_id']} 相同")
    return err, warn


def load_ledger(seed_path, runtime_path=None):
    """始终加载只读锚点种子；运行账本存在时按 sheet_id 合并，后者覆盖同名项。"""
    entries = json.load(open(seed_path, encoding="utf-8"))
    if runtime_path and os.path.exists(runtime_path):
        entries += json.load(open(runtime_path, encoding="utf-8"))
    merged = {}
    for i, item in enumerate(entries):
        merged[item.get("sheet_id", f"__anonymous_{i}")] = item
    return list(merged.values())


def entry(plan):
    return {
        "sheet_id": plan["sheet_id"],
        "seed": plan["seed"],
        "background": plan["page"]["background"],
        "layout": plan["page"]["layout"],
        "objects": [p["object"] for p in plan["pieces"]],
        "displaces": [p["displaces"] for p in plan["pieces"]],
        "slots": [[p["mechanism"], p["domain"]] for p in plan["pieces"]],
        "accents": [a.get("text") or a.get("motif") for a in plan["accents"]],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--ledger", default=None, help="调用项目的 ledger.json；锚点排除种子始终自动加载")
    ap.add_argument("--append", action="store_true", help="通过后把本页追加进调用项目 ledger（需要 --ledger）")
    a = ap.parse_args()
    if a.append and not a.ledger:
        ap.error("--append 需要同时提供 --ledger")

    plan = json.load(open(a.plan, encoding="utf-8"))
    here = os.path.dirname(os.path.abspath(__file__))
    schema = os.path.join(here, "..", "references", "sheet.schema.json")
    seed_ledger = os.path.join(here, "..", "references", "anchor-exclusions.json")

    err, degraded = check_schema(plan, schema)
    if degraded:
        print("  ! 未安装 jsonschema，已降级为最小字段检查（pip install jsonschema 可开启完整校验）")
    if not err:
        e2, w2 = check_structure(plan)
        ledger = load_ledger(seed_ledger, a.ledger)
        e3, w3 = check_ledger(plan, ledger)
        err, warn = e2 + e3, w2 + w3
    else:
        warn = []

    print(f"== {plan.get('sheet_id', a.plan)} ==")
    for x in err:
        print("  ✗", x)
    for x in warn:
        print("  !", x)
    print(f"\n{'拒收' if err else '通过'}：{len(err)} 项硬伤 / {len(warn)} 项提示")

    if err:
        return 1
    if a.append and a.ledger:
        ledger = [e for e in ledger if e.get("sheet_id") != plan["sheet_id"]] + [entry(plan)]
        os.makedirs(os.path.dirname(os.path.abspath(a.ledger)), exist_ok=True)
        json.dump(ledger, open(a.ledger, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"已追加进 ledger: {a.ledger}（共 {len(ledger)} 页）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
