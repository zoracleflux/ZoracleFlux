"""Fail-closed, transparent relation registry and deterministic validator."""

from __future__ import annotations

import ast
import inspect
import re
import time
from dataclasses import dataclass, asdict
from typing import Any, Callable

from . import transformations

Api = dict[str, Callable[..., Any]]
_TAG = re.compile(r"^\s*@relation(?:\s+(.*?))?\s*$", re.MULTILINE)


class RelationSpecError(ValueError):
    """The source contains an unknown or malformed relation declaration."""


@dataclass(frozen=True)
class Relation:
    name: str
    function_name: str
    tag: str
    description: str
    cases: tuple[Any, ...]
    check: Callable[[Api, Any], None]
    source: str

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result.pop("check", None)
        result["cases"] = len(self.cases)
        return result


def _norm_idempotent(api: Api, text: str) -> None:
    fn = api["normalize_whitespace"]
    assert fn(fn(text)) == fn(text)


def _norm_free(api: Api, text: str) -> None:
    out = api["normalize_whitespace"](text)
    assert " ".join(out.split()) == out


def _norm_tokens(api: Api, text: str) -> None:
    assert api["normalize_whitespace"](text).split() == text.split()


def _clamp_idempotent(api: Api, args: tuple[float, float, float]) -> None:
    value, low, high = args
    fn = api["clamp"]
    assert fn(fn(value, low, high), low, high) == fn(value, low, high)


def _clamp_bounded(api: Api, args: tuple[float, float, float]) -> None:
    value, low, high = args
    out = api["clamp"](value, low, high)
    assert low <= out <= high


def _clamp_endpoints(api: Api, args: tuple[float, float, float]) -> None:
    _, low, high = args
    fn = api["clamp"]
    assert fn(low, low, high) == low and fn(high, low, high) == high


def _rotate_composition(api: Api, args: tuple[tuple[int, ...], int, int]) -> None:
    items, left, right = args
    fn = api["rotate_left"]
    assert fn(fn(items, left), right) == fn(items, left + right)


def _rotate_length(api: Api, args: tuple[tuple[int, ...], int]) -> None:
    items, amount = args
    assert len(api["rotate_left"](items, amount)) == len(items)


def _unique_idempotent(api: Api, items: tuple[int, ...]) -> None:
    fn = api["stable_unique"]
    assert fn(fn(items)) == fn(items)


def _unique_membership(api: Api, items: tuple[int, ...]) -> None:
    assert set(api["stable_unique"](items)) == set(items)


def _unique_tuple(api: Api, items: tuple[int, ...]) -> None:
    assert isinstance(api["stable_unique"](items), tuple)


def _chunk_flatten(api: Api, args: tuple[tuple[int, ...], int]) -> None:
    items, size = args
    assert tuple(x for part in api["chunk"](items, size) for x in part) == items


def _chunk_size(api: Api, args: tuple[tuple[int, ...], int]) -> None:
    items, size = args
    assert all(0 < len(part) <= size for part in api["chunk"](items, size))


_ITEMS = ((), (1,), (1, 2, 1), (-2, 0, 3, 3), tuple(range(8)))
_TEXT = ("", " ", " a b ", "a\tb\n", "one  two", "alpha")
_BOUNDS = ((0, -1, 1), (4, 0, 2), (-3, -2, 7), (1.5, 1.5, 3.0))
_ROTATE = tuple((xs, n) for xs in _ITEMS for n in (-9, -1, 0, 1, 9))
_COMPOSE = tuple((xs, a, b) for xs in _ITEMS for a, b in ((-3, 2), (0, 4), (5, 7)))
_CHUNK = tuple((xs, n) for xs in _ITEMS for n in (1, 2, 4))

REGISTRY: dict[str, tuple[str, tuple[Any, ...], Callable[[Api, Any], None], str]] = {
    "idempotent": ("Applying the transformation twice equals applying it once.", _TEXT, _norm_idempotent, "template:v1"),
    "whitespace-free": ("The result is canonical whitespace.", _TEXT, _norm_free, "template:v1"),
    "token-preserving": ("Normalization preserves the token sequence.", _TEXT, _norm_tokens, "template:v1"),
    "bounded": ("A clamped value lies between inclusive bounds.", _BOUNDS, _clamp_bounded, "template:v1"),
    "endpoint-preserving": ("Clamping either endpoint preserves it.", _BOUNDS, _clamp_endpoints, "template:v1"),
    "composition": ("Sequential rotations compose by adding amounts.", _COMPOSE, _rotate_composition, "template:v1"),
    "length-preserving": ("Rotation does not change item count.", _ROTATE, _rotate_length, "template:v1"),
    "membership": ("Unique output has exactly input membership.", _ITEMS, _unique_membership, "template:v1"),
    "tuple-output": ("Unique output remains an immutable tuple.", _ITEMS, _unique_tuple, "template:v1"),
    "flatten-roundtrip": ("Flattening chunks reconstructs the original.", _CHUNK, _chunk_flatten, "template:v1"),
    "chunk-size": ("Chunks are non-empty and no larger than size.", _CHUNK, _chunk_size, "template:v1"),
}


def _declared_tags(doc: str | None) -> list[str]:
    tags: list[str] = []
    for match in _TAG.finditer(doc or ""):
        tag = (match.group(1) or "").strip()
        if not tag or not re.fullmatch(r"[a-z][a-z0-9-]*", tag):
            raise RelationSpecError("malformed @relation declaration; use @relation <known-tag>")
        tags.append(tag)
    # Catch lines beginning with @relation that the strict regex did not consume.
    for line in (doc or "").splitlines():
        if line.strip().startswith("@relation") and line.strip() not in {f"@relation {t}" for t in tags}:
            raise RelationSpecError(f"malformed @relation declaration: {line.strip()!r}")
    return tags


def discover_relations(module: Any = transformations) -> list[Relation]:
    found: list[Relation] = []
    for name, fn in inspect.getmembers(module, inspect.isfunction):
        if fn.__module__ != module.__name__:
            continue
        for tag in _declared_tags(inspect.getdoc(fn)):
            if tag not in REGISTRY:
                raise RelationSpecError(f"unknown relation tag {tag!r} on {name}")
            description, cases, check, source = REGISTRY[tag]
            found.append(Relation(f"{name}:{tag}", name, tag, description, cases, check,
                                  f"{module.__name__}.{name} docstring"))
    return found


def production_api() -> Api:
    return {name: getattr(transformations, name) for name in (
        "normalize_whitespace", "clamp", "rotate_left", "stable_unique", "chunk")}


def validate_relation(relation: Relation, api: Api, timeout_ms: int = 250) -> dict[str, Any]:
    started = time.perf_counter()
    for index, value in enumerate(relation.cases):
        if (time.perf_counter() - started) * 1000 > timeout_ms:
            return {"relation": relation.name, "status": "timeout", "case": index,
                    "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}
        try:
            relation.check(api, value)
        except Exception as exc:
            return {"relation": relation.name, "status": "failed", "case": index,
                    "error": f"{type(exc).__name__}: {exc}",
                    "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}
    return {"relation": relation.name, "status": "passed", "cases": len(relation.cases),
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}


def analyze_source(path: str) -> dict[str, Any]:
    """Parse source without importing or executing it."""
    source = open(path, "r", encoding="utf-8").read()
    tree = ast.parse(source, filename=path)
    declarations = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            declarations.extend({"function": node.name, "tag": t} for t in _declared_tags(doc))
    for item in declarations:
        if item["tag"] not in REGISTRY:
            raise RelationSpecError(f"unknown relation tag {item['tag']!r} on {item['function']}")
    return {"path": path, "executed": False, "declarations": declarations, "supported_tags": sorted(REGISTRY)}
