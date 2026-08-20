"""Domain assertions over MCP tool names, annotations, and call results.

Consumes a name set or a mapping ``name -> info`` where ``info`` has ``.name``
and ``.annotations``, or a dict with ``readOnlyHint``. No MCP SDK import.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping


def assert_tools_named(names: set[str], expected: set[str]) -> None:
    missing = expected - names
    extra = names - expected
    assert not missing and not extra, f"missing={missing} extra={extra}"


def assert_subset_named(names: set[str], required: set[str]) -> None:
    missing = required - names
    assert not missing, f"missing={missing}"


def _read_only_hint(info: Any) -> Any:
    annotations: Any = info
    if not isinstance(info, Mapping):
        annotations = getattr(info, "annotations", info)
    if isinstance(annotations, Mapping):
        if "readOnlyHint" in annotations:
            return annotations["readOnlyHint"]
        return annotations.get("read_only_hint")
    hint = getattr(annotations, "read_only_hint", None)
    if hint is None:
        hint = getattr(annotations, "readOnlyHint", None)
    return hint


def assert_tool_annotated_read_only(info: Any) -> None:
    hint = _read_only_hint(info)
    assert hint is True, f"expected readOnlyHint=True, got {hint!r}"


def assert_call_equals(actual: Any, expected: Any) -> None:
    assert actual == expected, f"call result {actual!r} != {expected!r}"


def names_from_registry(registry: Mapping[str, Any] | Iterable[str]) -> set[str]:
    if isinstance(registry, Mapping):
        return set(registry)
    return set(registry)
