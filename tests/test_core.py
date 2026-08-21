import types

from zoracleflux.mutants import run_mutations
from zoracleflux.relations import Relation, RelationSpecError, discover_relations, production_api, validate_relation
from zoracleflux.transformations import clamp, chunk, normalize_whitespace, rotate_left, stable_unique


def test_reference_functions_and_relations():
    assert normalize_whitespace(" a\tb ") == "a b"
    assert clamp(4, 0, 2) == 2
    assert rotate_left((1, 2, 3), 1) == (2, 3, 1)
    assert stable_unique((2, 1, 2)) == (2, 1)
    assert chunk((1, 2, 3), 2) == ((1, 2), (3,))
    relations = discover_relations()
    assert len(relations) == 13
    assert all(validate_relation(r, production_api())["status"] == "passed" for r in relations)


def test_mutation_suite_is_explicit_and_kills_all():
    results = run_mutations()
    assert len(results) == 5
    assert all(result["killed"] for result in results)


def test_unknown_relation_is_fail_closed():
    def bad():
        """@relation not-a-supported-tag"""
    bad.__module__ = "unknown"
    unknown = types.ModuleType("unknown")
    unknown.bad = bad
    try:
        discover_relations(unknown)
    except RelationSpecError as exc:
        assert "unknown relation tag" in str(exc)
    else:
        raise AssertionError("unknown relation was accepted")


def test_invalid_inputs_and_timeout_are_visible():
    import pytest
    with pytest.raises(ValueError):
        clamp(1, 3, 2)
    with pytest.raises(ValueError):
        chunk((1,), 0)
    with pytest.raises(AttributeError):
        normalize_whitespace(None)
    with pytest.raises(TypeError):
        rotate_left((1, 2), "bad")
    relation = Relation("synthetic:timeout", "synthetic", "timeout", "test", (1,), lambda api, value: None, "test")
    assert validate_relation(relation, production_api(), timeout_ms=0)["status"] == "timeout"
