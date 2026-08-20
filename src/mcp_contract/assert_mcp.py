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
    return _annotation_hint(info, "readOnlyHint", "read_only_hint")


def _destructive_hint(info: Any) -> Any:
    return _annotation_hint(info, "destructiveHint", "destructive_hint")


def _annotation_hint(info: Any, camel: str, snake: str) -> Any:
    annotations: Any = info
    if not isinstance(info, Mapping):
        annotations = getattr(info, "annotations", info)
    if isinstance(annotations, Mapping):
        if camel in annotations:
            return annotations[camel]
        return annotations.get(snake)
    hint = getattr(annotations, snake, None)
    if hint is None:
        hint = getattr(annotations, camel, None)
    return hint


def assert_tools_prefixed(names: Iterable[str], prefix: str) -> None:
    """Every tool name must start with ``prefix`` (e.g. ``swamp_``)."""
    bad = sorted(n for n in names if not n.startswith(prefix))
    assert not bad, f"tools not prefixed with {prefix!r}: {bad}"


def assert_tool_annotated_read_only(info: Any) -> None:
    hint = _read_only_hint(info)
    assert hint is True, f"expected readOnlyHint=True, got {hint!r}"


def assert_tool_annotated_non_destructive(info: Any) -> None:
    hint = _destructive_hint(info)
    assert hint is False, f"expected destructiveHint=False, got {hint!r}"


def non_readonly_tool_names(tools: Mapping[str, Any]) -> set[str]:
    """Return tool names explicitly marked ``readOnlyHint=False``."""
    return {name for name, tool in tools.items() if _read_only_hint(tool) is False}


def assert_non_readonly_tools_named(tools: Mapping[str, Any], expected: set[str]) -> None:
    """Pin the write-tool set — an unnoticed new write tool is the main risk."""
    actual = non_readonly_tool_names(tools)
    missing = expected - actual
    extra = actual - expected
    assert not missing and not extra, f"missing={missing} extra={extra}"


def assert_non_readonly_tools_non_destructive(
    tools: Mapping[str, Any],
    expected: set[str],
) -> None:
    """Write tools must be explicitly non-destructive (``destructiveHint=False``)."""
    assert_non_readonly_tools_named(tools, expected)
    for name in expected:
        assert_tool_annotated_non_destructive(tools[name])


def assert_call_equals(actual: Any, expected: Any) -> None:
    assert actual == expected, f"call result {actual!r} != {expected!r}"


def names_from_registry(registry: Mapping[str, Any] | Iterable[str]) -> set[str]:
    if isinstance(registry, Mapping):
        return set(registry)
    return set(registry)
