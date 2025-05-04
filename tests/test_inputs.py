"""Tests for the inputs module."""

from fluss_next.api.schema import PortInput, PortKind


def test_port() -> None:
    """Test the NodeException scalar."""
    PortInput(key="1234", kind=PortKind.INT, nullable=False)
