from __future__ import annotations

import os
from pathlib import Path

import pytest

from demo_server import server

FIXTURE = Path(__file__).parent / "fixtures" / "agent_check.jsonl"
os.environ.setdefault("SESSION_TRACE", str(FIXTURE))


@pytest.fixture
def mcp_server():
    return server
