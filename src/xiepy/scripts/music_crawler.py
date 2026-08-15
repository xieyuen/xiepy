from typing import Literal, TypedDict

from xiepy.common.exceptions import DependencyNotInstalled
from xiepy.common.logger import get_logger

try:
    import requests
    from jsonpath import jsonpath
except ModuleNotFoundError:
    raise DependencyNotInstalled(
        '脚本需要 requests 和 jsonpath, 请先安装依赖:\n'
        'pip install -U requests jsonpath',
    )

logger = get_logger(__name__)


class Param(TypedDict):
    input: str
    filter: Literal['name']
    type: Literal['netease', 'qq', 'kugou', 'kuwo', 'baidu', 'ximalaya']
    page: int
