import re
from typing import Any, NamedTuple, Protocol, runtime_checkable

from xiepy.utils.total_ordering import TotalOrderingGt


def compare_pre(pre: str, other: str) -> bool:
    """实现 semver 规则中对预发布版本号的比较"""

    pre_parts = pre.split(".") if pre else []
    other_parts = other.split(".") if other else []
    for p, o in zip(pre_parts, other_parts):
        if p.isdigit() and o.isdigit():
            if int(p) > int(o):
                return True
            elif int(p) < int(o):
                return False
        else:
            if p > o:
                return True
            elif p < o:
                return False
    return len(pre_parts) > len(other_parts)


@runtime_checkable
class VersionLikeObject(Protocol):
    major: int
    minor: int
    patch: int
    prerelease: str
    build: str

    @property
    def is_prerelease(self) -> bool:
        raise NotImplementedError


class VersionTuple(NamedTuple):
    major: int
    minor: int
    patch: int = 0
    prerelease: str = ""
    build: str = ""

    @property
    def is_prerelease(self) -> bool:
        return self.prerelease != ""

    def to_semver(self) -> SemanticVersion:
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.is_prerelease:
            s += f"-{self.prerelease}"
        if self.build:
            s += f"+{self.build}"
        return SemanticVersion(s)


type ValidTuple = tuple[int, int] | tuple[int, int, int] | tuple[int, int, int, str]
type ValidVersionType = VersionLikeObject | str | ValidTuple


class SemanticVersion(TotalOrderingGt[ValidVersionType]):
    major: int = 0
    """主版本号"""
    minor: int = 0
    """次版本号"""
    patch: int = 0
    """补丁版本号"""
    prerelease: str = ""
    """预发布版本号"""
    build: str = ""
    """构建元数据"""

    VERSION_PATTERN = re.compile(
        r"^(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$",
    )

    def __repr__(self):
        s = f"SemanticVersion(major={self.major}, minor={self.minor}, patch={self.patch}"

        if self.is_prerelease:
            s += f", prerelease={self.prerelease}"
        if self.build:
            s += f", build={self.build}"

        return s + ")"

    def __str__(self):
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    def __init__(self, version_str: str):
        if not isinstance(version_str, str):
            raise TypeError("Invalid version string")

        if not version_str:
            raise ValueError("Version string cannot be empty")

        match = self.VERSION_PATTERN.fullmatch(version_str)
        if not match:
            raise ValueError("Invalid version string")

        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3)) if match.group(3) else 0
        self.prerelease = match.group(4) or ""
        self.build = match.group(5) or ""

    @property
    def is_prerelease(self) -> bool:
        return self.prerelease != ""

    @staticmethod
    def __normalize(param: Any) -> VersionLikeObject:
        """实现比较的归一化, 保证支持多种类型的比较"""

        if isinstance(param, VersionLikeObject):
            return param
        elif isinstance(param, str):
            return SemanticVersion(param)
        elif isinstance(param, tuple):
            return VersionTuple(*param)  # type: ignore
        else:
            raise TypeError(f"Cannot compare semver with {type(param)}")

    def __eq__(self, other) -> bool:
        try:
            target = self.__normalize(other)
        except ValueError, TypeError:
            return False

        return all(
            [
                self.major == target.major,
                self.minor == target.minor,
                self.patch == target.patch,
                self.prerelease == target.prerelease,
            ],
        )

    def __gt__(self, other: ValidVersionType) -> bool:
        try:
            target = self.__normalize(other)
        except ValueError, TypeError:
            return NotImplemented

        if self.major > target.major:
            return True
        elif self.major < target.major:
            return False
        elif self.minor > target.minor:
            return True
        elif self.minor < target.minor:
            return False
        elif self.patch > target.patch:
            return True
        elif self.patch < target.patch:
            return False

        if not self.is_prerelease:
            return target.is_prerelease
        if not target.is_prerelease:
            return False

        return compare_pre(self.prerelease, target.prerelease)
