import pytest

from xiepy.utils.mcversion import MCVersion


@pytest.mark.parametrize(
    "ori, major, minor, patch, pre, build",
    [
        ("1.12.2", 1, 12, 2, "", ""),
        ("1.12", 1, 12, 0, "", ""),
        ("26.1", 26, 1, 0, "", ""),
        ("26.1-snapshot-1", 26, 1, 0, "snapshot-1", ""),
        ("26.1.1-snapshot-1", 26, 1, 1, "snapshot-1", ""),
        ("26.1.1", 26, 1, 1, "", ""),
        ("26.1.1+a", 26, 1, 1, "", "a"),
        ("26.1+bedrock", 26, 1, 0, "", "bedrock"),
    ],
)
def test_init(ori: str, major: int, minor: int, patch: int, pre: str, build: str):
    v = MCVersion(ori)
    is_prerelease: bool = bool(pre)

    assert v.major == major
    assert v.minor == minor
    assert v.patch == patch
    assert v.is_prerelease == is_prerelease
    assert v.prerelease == pre
    assert v.build == build


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

get_comparison_params = lambda exp: [(*p, e) for p, e in zip(param, exp)]


@pytest.mark.parametrize("a, b, expected", get_comparison_params(lt_expected))
def test_lt(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a < mcv_b) is expected
    assert (a < mcv_b) is expected
    assert (mcv_a < b) is expected


@pytest.mark.parametrize("a, b, expected", get_comparison_params(le_expected))
def test_le(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a <= mcv_b) is expected
    assert (a <= mcv_b) is expected
    assert (mcv_a <= b) is expected


@pytest.mark.parametrize("a, b, expected", get_comparison_params(gt_expected))
def test_gt(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a > mcv_b) is expected
    assert (a > mcv_b) is expected
    assert (mcv_a > b) is expected


@pytest.mark.parametrize("a, b, expected", get_comparison_params(ge_expected))
def test_ge(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a >= mcv_b) is expected
    assert (a >= mcv_b) is expected
    assert (mcv_a >= b) is expected


@pytest.mark.parametrize("a, b, expected", get_comparison_params(eq_expected))
def test_eq(a: str, b: str, expected: bool):
    mcv_a = MCVersion(a)
    mcv_b = MCVersion(b)

    assert (mcv_a == mcv_b) is expected
    assert (a == mcv_b) is expected
    assert (mcv_a == b) is expected
