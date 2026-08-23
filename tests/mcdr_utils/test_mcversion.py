import pytest

from xiepy.utils.mcversion import MCVersion

param: list[tuple[str, str]] = [
    ("1.13", "1.12"),
    ("1.14", "1.12"),
    ("26.1", "1.12"),
    ("26.1.1", "1.12"),
    ("1.12", "1.13"),
    ("1.12", "1.14"),
    ("1.12", "26.1"),
    ("1.12", "26.1.1"),
    ("1.13", "1.13"),
]
lt_expected: list[bool] = [False] * 4 + [True] * 4 + [False]
le_expected: list[bool] = [False] * 4 + [True] * 5
gt_expected: list[bool] = [True] * 4 + [False] * 5
ge_expected: list[bool] = [True] * 4 + [False] * 4 + [True]
eq_expected: list[bool] = [False] * 8 + [True]

get_args = lambda exp: [(*p, e) for p, e in zip(param, exp)]


@pytest.mark.parametrize("a, b, expected", get_args(lt_expected))
def test_lt(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a < mcv_b) is expected
    assert (a < mcv_b) is expected
    assert (mcv_a < b) is expected


@pytest.mark.parametrize("a, b, expected", get_args(le_expected))
def test_le(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a <= mcv_b) is expected
    assert (a <= mcv_b) is expected
    assert (mcv_a <= b) is expected


@pytest.mark.parametrize("a, b, expected", get_args(gt_expected))
def test_gt(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a > mcv_b) is expected
    assert (a > mcv_b) is expected
    assert (mcv_a > b) is expected


@pytest.mark.parametrize("a, b, expected", get_args(ge_expected))
def test_ge(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a >= mcv_b) is expected
    assert (a >= mcv_b) is expected
    assert (mcv_a >= b) is expected


@pytest.mark.parametrize("a, b, expected", get_args(eq_expected))
def test_eq(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a == mcv_b) is expected
    assert (a == mcv_b) is expected
    assert (mcv_a == b) is expected
