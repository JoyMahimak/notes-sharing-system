import pytest

@pytest.mark.skip(reason="Skipping Selenium in CI (no server running)")
def test_selenium():
    pass