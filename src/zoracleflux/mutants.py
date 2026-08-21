"""Bounded mutation checks for the trusted built-in fixture only.

Mutants are explicit Python callables, not compiled or executed source text.
External source mutation is intentionally unsupported.
"""

from __future__ import annotations

from .relations import discover_relations, validate_relation


def _mutant_api(mutant: str):
    from . import transformations as t
    api = {name: getattr(t, name) for name in ("normalize_whitespace", "clamp", "rotate_left", "stable_unique", "chunk")}
    if mutant == "M01":
        api["normalize_whitespace"] = lambda text: "".join(text.split())
    elif mutant == "M02":
        api["clamp"] = lambda value, low, high: max(low + 1, min(value, high))
    elif mutant == "M03":
        api["rotate_left"] = lambda items, amount: items[(amount % len(items)) + 1:] + items[:amount % len(items)] if items else items
    elif mutant == "M04":
        api["stable_unique"] = lambda items: list(items)
    elif mutant == "M05":
        api["chunk"] = lambda items, size: tuple(items[index:index + size - 1] for index in range(0, len(items), size))
    else:
        raise ValueError(f"unknown trusted mutant {mutant}")
    return api


def run_mutations() -> list[dict]:
    relations = discover_relations()
    results = []
    for mutant in ("M01", "M02", "M03", "M04", "M05"):
        api = _mutant_api(mutant)
        killed_by = []
        for relation in relations:
            if validate_relation(relation, api)["status"] != "passed":
                killed_by.append(relation.name)
        results.append({"mutant": mutant, "killed": bool(killed_by), "killed_by": killed_by})
    return results
