import json
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "Data" / "Card.json"
    out = repo_root / "tools" / "CardEffects.json"

    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data.get("Cards", [])
    extracted = []

    for c in cards:
        # Preserve a predictable key order for readability
        item = {
            "Name": c.get("Name", ""),
            "ID": c.get("ID", ""),
            "EffectDescription": c.get("EffectDescription", ""),
            "EffectString": c.get("EffectString", ""),
        }
        extracted.append(item)

    with out.open("w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(extracted)} card effects to {out}")


if __name__ == "__main__":
    main()

