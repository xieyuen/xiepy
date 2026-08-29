import pytest

from xiepy.utils.semver import SemanticVersion, VersionTuple, compare_pre


@pytest.mark.parametrize(
    "version, major, minor, patch, prerelease, build",
    [
        ("1.2.3", 1, 2, 3, "", ""),
        ("1.2", 1, 2, 0, "", ""),
        ("1.2.3-alpha", 1, 2, 3, "alpha", ""),
        ("1.2.3-alpha.1", 1, 2, 3, "alpha.1", ""),
        ("1.2.3+build.7", 1, 2, 3, "", "build.7"),
        ("1.2.3-alpha+build.7", 1, 2, 3, "alpha", "build.7"),
    ],
)
def test_init(
    version: str, major: int, minor: int, patch: int, prerelease: str, build: str
):
    v = SemanticVersion(version)

    assert v.major == major
    assert v.minor == minor
    assert v.patch == patch
    assert v.prerelease == prerelease
    assert v.build == build
    assert v.is_prerelease is bool(prerelease)


@pytest.mark.parametrize(
    "version",
    [
        "",
        "v1.2.3",
        "1",
        "1.2.3-",
        "1.2.3+",
        "1.2.3-alpha..1",
        "1.2.3-alpha+",
        "1.2.3#abc",
    ],
)
def test_init_invalid(version: str):
    with pytest.raises((TypeError, ValueError)):
        SemanticVersion(version)


@pytest.mark.parametrize(
    "pre, other, expected",
    [
        ("alpha", "beta", False),
        ("beta", "alpha", True),
        ("1.0", "0.9", True),
        ("0.9", "1.0", False),
        ("alpha.1", "alpha.beta", False),
        ("alpha.beta", "alpha.1", True),
        ("alpha", "alpha", False),
        ("alpha.1", "alpha.1", False),
        ("alpha.1", "alpha", True),
        ("alpha", "alpha.1", False),
    ],
)
def test_compare_pre(pre: str, other: str, expected: bool):
    assert compare_pre(pre, other) is expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ("1.0.0", "1.0.0", False),
        ("1.0.0", "1.0.1", False),
        ("1.0.1", "1.0.0", True),
        ("1.0.0-alpha", "1.0.0", False),
        ("1.0.0", "1.0.0-alpha", True),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta", False),
        ("1.0.0-alpha.beta", "1.0.0-alpha.1", True),
        ("1.0.0-beta", "1.0.0-beta.2", False),
        ("1.0.0-beta.2", "1.0.0-beta.11", False),
        ("1.0.0-beta.11", "1.0.0-beta.2", True),
        ("1.0.0-rc.1", "1.0.0", False),
    ],
)
def test_compare(left: str, right: str, expected: bool):
    left_v = SemanticVersion(left)
    right_v = SemanticVersion(right)

    assert (left_v > right_v) is expected
    assert (left_v > right) is expected
    assert (left > right_v) is expected

    assert (left_v >= right_v) is (expected or left_v == right_v)
    assert (left >= right_v) is (expected or left_v == right_v)
    assert (left_v >= right) is (expected or left_v == right_v)

    assert (left_v < right_v) is (not expected and left_v != right_v)
    assert (left < right_v) is (not expected and left_v != right_v)
    assert (left_v < right) is (not expected and left_v != right_v)

    assert (left_v <= right_v) is (not expected or left_v == right_v)
    assert (left <= right_v) is (not expected or left_v == right_v)
    assert (left_v <= right) is (not expected or left_v == right_v)

    assert (left_v == right_v) is (left == right)
    assert (left == right_v) is (left == right)
    assert (left_v == right) is (left == right)


@pytest.mark.parametrize(
    "version, value, expected",
    [
        ("1.2.3", "1.2.3", True),
        ("1.2.3", (1, 2, 3), True),
        ("1.2.3", (1, 2, 3, "alpha"), False),
        ("1.2.3-alpha", "1.2.3-alpha", True),
        ("1.2.3-alpha", (1, 2, 3, "alpha"), True),
        ("1.2.3-alpha", (1, 2, 3, "beta"), False),
    ],
)
def test_equality(version: str, value, expected: bool):
    v = SemanticVersion(version)

    assert (v == value) is expected
    assert (value == v) is expected


@pytest.mark.parametrize(
    "version, expected",
    [
        (VersionTuple(1, 2, 3), "1.2.3"),
        (VersionTuple(1, 2, 3, "alpha"), "1.2.3-alpha"),
    ],
)
def test_to_semver_and_str(version, expected: str):
    s = version.to_semver()

    assert str(s) == expected


@pytest.mark.parametrize(
    "version, expected",
    [
        ("1.2.3", "1.2.3"),
        ("1.2.3-alpha", "1.2.3-alpha"),
        ("1.2.3+build.7", "1.2.3+build.7"),
        ("1.2.3-alpha+build.7", "1.2.3-alpha+build.7"),
    ],
)
def test_str(version, expected: str):
    s = SemanticVersion(version)

    assert str(s) == expected
