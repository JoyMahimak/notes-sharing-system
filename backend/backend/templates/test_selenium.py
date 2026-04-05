import pytest

# This test is skipped in CI/CD because browser is not available
@pytest.mark.skip(reason="Skipping Selenium in CI")
def test_selenium():
    pass