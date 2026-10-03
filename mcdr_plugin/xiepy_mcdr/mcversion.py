"""
Minecraft 版本解析
=================

Introduction
------------

此模块来自 MCDRpost 源码, 最初是为了实现 Minecraft 版本的先后比较而写的,
逐步修改形成一个较为完整的版本解析类.

目前支持旧版本系统的所有正式版本号和新版本系统的所有版本号 (正式或快照) 之间的比较.
旧的快照由于过于复杂且已被 Mojang 官方弃用, 故不考虑兼容.

基本原理
-------

Minecraft 的版本号有两种命名系统:

1) 旧版: 正式版采用类 semver 的命名系统, 例如 1.7.10, 1.8.9, 1.12.2 等等;
    快照版则采用年份和第几周 (如 13 年第 41 周的快照为 13w41a) 的命名系统.
2) 新版: 正式版采用年份和版本的命名系统, 如 26 年第一个版本为 26.1, 它的补丁版本为 26.1.1;
    快照版本采用对应正式版的版本号加上 ``-snapshot-`` 和快照版本数的后缀,
    如 26 年第一个版本的第一个快照为 26.1-snapshot-1, 第二个快照为 26.1-snapshot-2, 以此类推.

由于新版本命名系统和旧的正式版十分接近 semver, 所以我们按照 semver 的规则解析并实现比较.

.. versionchanged:: 0.1.2
    把 semver 的部分迁移至单独的模块
"""

import re
from typing import Any

from xiepy.utils.semver import VersionLikeObject, compare_pre
from xiepy.utils.total_ordering import TotalOrderingGt

type ValidTuple = tuple[int, int] | tuple[int, int, int] | tuple[int, int, int, str]
type ComparableType = VersionLikeObject | str | ValidTuple


class MCVersion(TotalOrderingGt[ComparableType]):
    """Minecraft 版本解析类

    此类实现了 Minecraft 版本的解析, 无论是新命名系统还是旧系统, 都可以正确解析.
    并且此类实现了版本之间的比较. 不仅限于 MCVersion 实例,
    还可以与合法的版本字符串和合法的 tuple 实例比较.
    """

    major: int = 0
    """主版本号"""
    minor: int = 0
    """次版本号"""
    patch: int = 0
    """补丁版本号"""
    prerelease: str = ""
    """预发布版本号, 会包含 ``snapshot-`` 前缀"""
    build: str = ""
    """构建元数据, 一般的 Minecraft: Java Edition 不应有这一项"""

    VERSION_PATTERN = re.compile(
        r"^(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$",
    )

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

    def __repr__(self):
        s = f"MCVersion(major={self.major}, minor={self.minor}, patch={self.patch}"

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

    @staticmethod
    def __normalize(param: Any) -> VersionLikeObject:
        """实现比较的归一化, 保证支持 MCVersion, str, tuple 三种类型的比较"""

        if isinstance(param, VersionLikeObject):
            return param
        elif isinstance(param, str):
            return MCVersion(param)
        elif isinstance(param, tuple):
            return VersionTuple(*param)  # type: ignore
        else:
            raise TypeError(f"Cannot compare MCVersion with {type(param)}")

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

    def __gt__(self, other) -> bool:
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
