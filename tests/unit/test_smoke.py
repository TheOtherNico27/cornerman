"""Smoke tests: prove the package and its parts can be imported.

If these fail, nothing else can work, so they are the first thing CI runs.
"""

import importlib

import pytest

import cornerman

SUBPACKAGES = ["api", "worker", "detector", "common", "gateway"]


def test_package_imports() -> None:
    assert cornerman.__name__ == "cornerman"


@pytest.mark.parametrize("name", SUBPACKAGES)
def test_subpackage_imports(name: str) -> None:
    module = importlib.import_module(f"cornerman.{name}")
    assert module.__name__ == f"cornerman.{name}"
