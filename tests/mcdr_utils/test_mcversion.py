import pytest

from xiepy.utils.mcversion import MCVersion

param: list[tuple[str, str, bool]] = [
    ("1.13", "1.12", False),
    ("1.14", "1.12", False),
    ("26.1", "1.12", False),
    ("26.1.1", "1.12", False),
    ("1.12","1.13", True),
    ("1.12","1.14", True),
    ("1.12","26.1", True),
    ("1.12","26.1.1", True),
]


@pytest.mark.parametrize("a, b, expected", param)
def test_lt(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a < mcv_b) is expected
    assert (a < mcv_b) is expected
    assert (mcv_a < b) is expected
