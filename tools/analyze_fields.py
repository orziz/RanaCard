#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Data"


def load(path: Path) -> Dict[str, Any]:
    with path.open("rb") as f:
        return json.load(f)


def normalize(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def analyze(items: List[Dict[str, Any]]) -> Tuple[List[str], List[Tuple[str, int, int, int, List[str]]]]:
    total = len(items)
    keys = set()
    for it in items:
        if isinstance(it, dict):
            keys.update(it.keys())

    uniform: List[str] = []
    varying: List[Tuple[str, int, int, int, List[str]]] = []

    for k in sorted(keys):
        present = 0
        uniq = {}
        for it in items:
            if isinstance(it, dict) and k in it:
                present += 1
                uniq.setdefault(normalize(it[k]), 0)
                uniq[normalize(it[k])] += 1
        if present == total and len(uniq) == 1:
            uniform.append(k)
        else:
            # collect up to 5 example values
            samples = list(uniq.keys())[:5]
            varying.append((k, present, total - present, len(uniq), samples))

    return uniform, varying


def report(title: str, items: List[Dict[str, Any]]):
    uniform, varying = analyze(items)
    print(f"=== {title} ===")
    print(f"总条目: {len(items)}")
    print(f"字段总数: {len(uniform) + len(varying)}")
    print(f"- 全部相同(可隐藏): {len(uniform)}")
    if uniform:
        print("  "+", ".join(uniform))
    print(f"- 存在差异(应展示): {len(varying)}")
    for k, present, missing, uniq_count, samples in varying:
        smp = "; ".join(samples)
        print(f"  · {k}: 出现 {present}, 缺失 {missing}, 不同值 {uniq_count}; 示例: {smp}")
    print()


def main():
    card = load(DATA / "Card.json")
    pend = load(DATA / "Pendant.json")
    if not isinstance(card, dict) or not isinstance(card.get("Cards"), list):
        raise SystemExit("Card.json 格式不正确：缺少 Cards 数组")
    if not isinstance(pend, dict) or not isinstance(pend.get("Pendant"), list):
        raise SystemExit("Pendant.json 格式不正确：缺少 Pendant 数组")
    report("Card.Cards[*]", card["Cards"])
    report("Pendant.Pendant[*]", pend["Pendant"])


if __name__ == "__main__":
    main()

