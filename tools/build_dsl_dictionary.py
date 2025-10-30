import json
import re
from pathlib import Path


CLAUSE_SPLIT = re.compile(r"\s*#\s*")
ANGLE_BLOCK = re.compile(r"<([^>]*)>")
PARENS = re.compile(r"\(([^)]*)\)")
FUNC = re.compile(r"\b([A-Za-z][A-Za-z0-9_]*)\((.*)\)$")


def extract_dictionary(items):
    events = set()
    tags = set()
    functions = set()
    comparators = set()
    targets = set()
    properties = set()
    value_funcs = set()

    def add_target(tok: str):
        if not tok:
            return
        if tok in {
            'Self','SelfCard','SelfPendant','Global','Chosen','Left','Right','Around','AroundHarvest','Land',
            'CardCollection','Bag','BackBag','Hand','Deck','Grave','Shop','Target','All','Any','None'
        } or 'Card' in tok:
            targets.add(tok)

    def add_comp(op: str):
        if op in {
            'Is','IsNot','Not','Contain','NotContain','Bigger','BiggerOrEqual','Smaller','SmallerOrEqual','Equal'
        }:
            comparators.add(op)

    for row in items:
        s = (row.get('EffectString') or '').strip()
        if not s or s == '--':
            continue
        for clause in CLAUSE_SPLIT.split(s):
            clause = clause.strip()
            if not clause:
                continue
            m = re.match(r"^([A-Za-z]+(?:\([^)]+\))?)", clause)
            if m:
                events.add(m.group(1))

            angle_contents = ANGLE_BLOCK.findall(clause)
            stripped = ANGLE_BLOCK.sub('', clause)
            for tm in PARENS.finditer(stripped):
                tag = tm.group(1).strip()
                if tag:
                    tags.add(tag)

            for content in angle_contents:
                for cond in re.findall(r"\{([^}]*)\}", content):
                    parts = [p.strip() for p in re.split(r",", cond)]
                    if len(parts) >= 3:
                        add_target(parts[0])
                        properties.add(parts[1])
                        add_comp(parts[2])
                    for token in parts[3:]:
                        fm = FUNC.match(token)
                        if fm:
                            value_funcs.add(fm.group(1))
                for seg in re.findall(r"\[([^\]]*)\]", content):
                    fm = FUNC.match(seg.strip())
                    if fm:
                        functions.add(fm.group(1))
                        args = fm.group(2)
                        for a in re.split(r"[;,]", args):
                            a = a.strip()
                            if not a:
                                continue
                            nf = FUNC.match(a)
                            if nf:
                                value_funcs.add(nf.group(1))
                                continue
                            add_target(a)
                    else:
                        parts = [p.strip() for p in re.split(r",", seg)]
                        if parts:
                            add_target(parts[0])
                        if len(parts) >= 2:
                            properties.add(parts[1])
                        if len(parts) >= 3:
                            if not parts[2].startswith('='):
                                gm = FUNC.match(parts[2])
                                if gm:
                                    value_funcs.add(gm.group(1))

    return {
        'events': events,
        'tags': tags,
        'functions': functions,
        'comparators': comparators,
        'targets': targets,
        'properties': properties,
        'value_functions': value_funcs,
    }


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    card_src = repo / 'Data' / 'Card.json'
    pendant_src = repo / 'Data' / 'Pendant.json'
    out = repo / 'ui' / 'src' / 'assets' / 'dsl_dictionary.json'
    out.parent.mkdir(parents=True, exist_ok=True)

    cards = json.load(card_src.open('r', encoding='utf-8')).get('Cards', [])
    pj = json.load(pendant_src.open('r', encoding='utf-8'))
    pendants = pj.get('Pendants') or pj.get('Pendant') or []

    d_cards = extract_dictionary(cards)
    d_pendants = extract_dictionary(pendants)

    merged: dict[str, dict[str, list[str]]] = {}
    for k in d_cards.keys():
        s_card = d_cards[k]
        s_pen = d_pendants[k]
        both = sorted(s_card & s_pen)
        card_only = sorted(s_card - s_pen)
        pendant_only = sorted(s_pen - s_card)
        merged[k] = {
            'both': both,
            'card_only': card_only,
            'pendant_only': pendant_only,
        }

    json.dump(merged, out.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'Wrote DSL dictionary (with sources) to {out}')


if __name__ == '__main__':
    main()

