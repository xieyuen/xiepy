"""
重构我当年抄的脚本
"""

import dataclasses
from pathlib import Path
from typing import Iterable

from xiepy.common.constants import WORKING_DIRECTORY
from xiepy.common.exceptions import DependencyNotInstalled
from xiepy.common.logger import get_logger

try:
    import requests
    from jsonpath import jsonpath
except ModuleNotFoundError:
    raise DependencyNotInstalled(
        "脚本需要 requests 和 jsonpath, 请先安装依赖: "
        "pip install -U requests jsonpath",
    )

logger = get_logger(__name__)

AVAILABLE_PLATFORMS: list[str] = [
    "netease",
    "qq",
    "kugou",
    "kuwo",
    "baidu",
    "ximalaya",
]
TARGET_URL: str = "https://music.liuzhijin.cn/"
HEADERS: dict[str, str] = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/87.0.4280.141 Safari/537.36",
    # 判断请求是异步还是同步
    "x-requested-with": "XMLHttpRequest",
}


@dataclasses.dataclass
class SearchResult:
    titles: list[str]
    authors: list[str]
    urls: list[str]

    @property
    def length(self) -> int:
        return len(self.titles)

    def zip_iter(self) -> Iterable[tuple[str, str, str]]:
        return zip(self.titles, self.authors, self.urls)


def download(
    url: str,
    author: str,
    title: str,
    *,
    path: Path = WORKING_DIRECTORY,
) -> None:
    logger.info(f"{author}-{title} 正在下载...")

    path.mkdir(parents=True, exist_ok=True)

    with (path / f"{title}-{author}.mp3").open("wb") as f:
        f.write(requests.get(url).content)


def search(name: str, platform: str) -> SearchResult:
    json_text = requests.post(
        TARGET_URL,
        {
            "input": name,
            "filter": "name",
            "type": platform,
            "page": 1,
        },
        headers=HEADERS,
    ).json()

    titles: list[str] = jsonpath(json_text, "$..title")
    authors: list[str] = jsonpath(json_text, "$..author")
    urls: list[str] = jsonpath(json_text, "$..url")

    return SearchResult(titles=titles, authors=authors, urls=urls)


def notification() -> None:
    logger.info("此脚本支持网易云、QQ、酷狗、酷我、百度和喜马拉雅的音乐")
    logger.info("搜索技术由 `https://music.liuzhijin.cn/` 提供支持")
    logger.warning("脚本有较长时间未维护, 可能存在无法使用的情况")
    logger.warning("仅供学习参考, 请勿用于商业用途")


def main() -> None:
    notification()
    name: str = input("请输入歌曲名: ")
    platforms_info: tuple = (
        "1.网易云:netease",
        "2.QQ:qq",
        "3.酷狗:kugou",
        "4.酷我:kuwo",
        "5.百度:baidu",
        "6.喜马拉雅:ximalaya",
    )

    logger.info("脚本支持以下平台:")
    for plat in platforms_info:
        logger.info(plat)

    platforms: list[str] = input("请选择平台(可多个,用英文逗号隔开): ").split(",")

    results: list = []

    for plat in platforms:
        if plat not in AVAILABLE_PLATFORMS:
            logger.warning(f"不支持的平台: {plat}, 跳过")
            continue
        res = search(name, plat)

        if res.length == 0:
            logger.warning(f"未在平台 {plat} 中查找到歌曲, 跳过")
            continue

        results.append(res)
        logger.info(f"平台 {plat} 的搜索结果如下:")

        for t, a, _ in res.zip_iter():
            logger.info(f"{t} - {a}")


if __name__ == "__main__":
    raise NotImplementedError
    main()
