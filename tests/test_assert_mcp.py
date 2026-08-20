"""Assertion helpers must work with no MCP SDK installed."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from mcp_contract.assert_mcp import (
    assert_call_equals,
    assert_non_readonly_tools_named,
    assert_non_readonly_tools_non_destructive,
    assert_subset_named,
    assert_tool_annotated_non_destructive,
    assert_tool_annotated_read_only,
    assert_tools_named,
    assert_tools_prefixed,
    non_readonly_tool_names,
)

SWAMP_TOOLS = {
    "swamp_estate_status",
    "swamp_whats_down",
    "swamp_findings",
    "swamp_service_history",
    "swamp_portal_status",
    "swamp_scheduled_tasks",
    "swamp_jobs_status",
    "swamp_kb_search",
    "swamp_enqueue_job",
    "swamp_run_repo_backup",
    "swamp_backup_build_image",
    "swamp_open_maintenance_window",
    "swamp_discussions_status",
    "swamp_post_discussion",
}


def test_assert_tools_named_exact_match():
    assert_tools_named(set(SWAMP_TOOLS), SWAMP_TOOLS)


def test_assert_tools_named_reports_missing_and_extra():
    names = {"swamp_estate_status", "bonus"}
    with pytest.raises(AssertionError, match="missing=") as exc:
        assert_tools_named(names, {"swamp_estate_status", "swamp_whats_down"})
    msg = str(exc.value)
    assert "swamp_whats_down" in msg
    assert "bonus" in msg
    assert "extra=" in msg


def test_assert_subset_named_allows_extras():
    assert_subset_named(SWAMP_TOOLS | {"future_tool"}, {"swamp_estate_status"})


def test_assert_subset_named_reports_missing():
    with pytest.raises(AssertionError, match="missing="):
        assert_subset_named({"swamp_estate_status"}, {"swamp_whats_down"})


def test_assert_tool_annotated_read_only_attr_and_dict():
    assert_tool_annotated_read_only(
        SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=True))
    )
    assert_tool_annotated_read_only(
        SimpleNamespace(annotations=SimpleNamespace(read_only_hint=True))
    )
    assert_tool_annotated_read_only({"readOnlyHint": True})


def test_assert_tool_annotated_read_only_rejects_write():
    with pytest.raises(AssertionError):
        assert_tool_annotated_read_only(
            SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=False))
        )


def test_assert_call_equals():
    assert_call_equals("hi", "hi")
    with pytest.raises(AssertionError):
        assert_call_equals("hi", "bye")


def test_non_readonly_tool_names_ignores_unmarked_and_read_only():
    tools = {
        "read": SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=True)),
        "write": SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=False)),
        "legacy": SimpleNamespace(annotations=SimpleNamespace(read_only_hint=False)),
        "unmarked": SimpleNamespace(annotations=None),
    }
    assert non_readonly_tool_names(tools) == {"write", "legacy"}


def test_assert_non_readonly_tools_named_exact_match():
    tools = {
        "write": SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=False)),
    }
    assert_non_readonly_tools_named(tools, {"write"})


def test_assert_non_readonly_tools_named_reports_missing_and_extra():
    tools = {
        "write_a": SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=False)),
        "write_b": SimpleNamespace(annotations=SimpleNamespace(readOnlyHint=False)),
    }
    with pytest.raises(AssertionError, match="missing=") as exc:
        assert_non_readonly_tools_named(tools, {"write_a"})
    msg = str(exc.value)
    assert "write_b" in msg
    assert "extra=" in msg


def test_assert_tools_prefixed_passes():
    assert_tools_prefixed({"swamp_a", "swamp_b"}, "swamp_")


def test_assert_tools_prefixed_reports_bad_names():
    with pytest.raises(AssertionError, match="swamp_"):
        assert_tools_prefixed({"swamp_ok", "other"}, "swamp_")


def test_assert_tool_annotated_non_destructive():
    assert_tool_annotated_non_destructive(
        SimpleNamespace(annotations=SimpleNamespace(destructiveHint=False))
    )
    assert_tool_annotated_non_destructive({"destructiveHint": False})


def test_assert_tool_annotated_non_destructive_rejects_destructive():
    with pytest.raises(AssertionError, match="destructiveHint=False"):
        assert_tool_annotated_non_destructive(
            SimpleNamespace(annotations=SimpleNamespace(destructiveHint=True))
        )


def test_assert_non_readonly_tools_non_destructive():
    tools = {
        "write": SimpleNamespace(
            annotations=SimpleNamespace(
                readOnlyHint=False,
                destructiveHint=False,
            )
        ),
    }
    assert_non_readonly_tools_non_destructive(tools, {"write"})


def test_assert_non_readonly_tools_non_destructive_rejects_destructive_write():
    tools = {
        "write": SimpleNamespace(
            annotations=SimpleNamespace(
                readOnlyHint=False,
                destructiveHint=True,
            )
        ),
    }
    with pytest.raises(AssertionError, match="destructiveHint=False"):
        assert_non_readonly_tools_non_destructive(tools, {"write"})
