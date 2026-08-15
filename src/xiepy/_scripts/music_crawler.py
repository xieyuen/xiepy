"""
Music Crawler

支持网易云、QQ、酷狗、酷我、百度和喜马拉雅
搜索技术由 `https://music.liuzhijin.cn/` 提供支持
"""

import os
from typing import TypedDict, Literal

import requests
from jsonpath import jsonpath


class Constants:
    musicNotFoundMsg = "对不起，暂无搜索结果!"
    defaultSavePath = './'
    searchURL = 'https://music.liuzhijin.cn/'
    headers = {
        "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/87.0.4280.141 Safari/537.36",
        # 判断请求是异步还是同步
        "x-requested-with": "XMLHttpRequest",
    }
    platformInfo = (
        "1.网易云:netease\n"
        "2.QQ:qq\n"
        "3.酷狗:kugou\n"
        "4.酷我:kuwo\n"
        "5.百度:baidu\n"
        "6.喜马拉雅:ximalaya"
    )
    platformMap = {
        k: v for keys, v in (
            (
                (
                    '1', 'n', 'net', 'wy', 'wyy', 'wangyi', 'wangyiyun', 'netease', '网易', '网易云', '网易云音乐'
                ), 'netease'
            ), (
                (
                    '2', 'q', 'qq', 'qqmusic', 'qqyinyue', 'qq音乐', 'qq 音乐'
                ), 'qq'
            ), (
                (
                    '3', 'kg', 'ku', 'kou', 'gou', 'kugou', '酷狗'
                ), 'kugou'
            ), (
                (
                    '4', 'kw', 'ko', 'wo', 'kuwo', '酷我'
                ), 'kuwo'
            ), (
                (
                    '5', 'b', 'bd', 'bu', 'baidu', '百度'
                ), 'baidu'
            ), (
                (
                    '6', 'x', 'xi', 'xmly', 'xmla', 'ximalaya', '喜马拉雅'
                ), 'ximalaya'
            ),
        ) for k in keys
    }


class Param(TypedDict):
    input: str
    filter: Literal['name']
    type: Literal['netease', 'qq', 'kugou', 'kuwo', 'baidu', 'ximalaya']
    page: int


class Crawler:
    @staticmethod
    def getParam(name: str, platform: str) -> Param:
        return {
            "input": name,
            "filter": "name",
            "type": Constants.platformMap[platform],
            "page": 1,
        }

    @staticmethod
    @curry
    def download(url, author, title, *, path):
        print(f'{author}-{title} 正在下载...')
        with open(f"{path}/{title}-{author}.mp3", mode='wb') as f:
            f.write(requests.get(url).content)

    def main(self):
        name = input("请输入歌曲名:")
        platforms = input(
            f"脚本支持以下平台:\n{Constants.platformInfo}\n请选择平台(可多个,用英文逗号隔开): "
        ).split(',')

        titles = []
        authors = []
        urls = []

        for platform in platforms:
            param = self.getParam(
                name=name,
                platform=platform
            )
            json_text = requests.post(
                url=Constants.searchURL,
                data=param,
                headers=Constants.headers,
            ).json()

            titles.append(jsonpath(json_text, '$..title'))
            authors.append(jsonpath(json_text, '$..author'))
            urls.append(jsonpath(json_text, '$..url'))

        if not titles[0]:
            raise MusicNotFoundError(Constants.musicNotFoundMsg)

        print("-------------------------------------------------------\n查找到以下歌曲:\n")

        index = 1
        shouldIgnores = []
        for i, (platform, tits, diffAuthor) in enumerate(zip(platforms, titles, authors)):
            if not diffAuthor:
                print(f'未在{platform}平台查询到歌曲')
                shouldIgnores.append(i)
                continue
            print(f"{platform}平台:")
            for t, a in zip(tits, diffAuthor):
                print(f"{index} | {t} - {a}")
                index += 1  # index++

        titles = [i for ind, item in enumerate(titles) if ind not in shouldIgnores for i in item]
        authors = [i for ind, item in enumerate(authors) if ind not in shouldIgnores for i in item]
        urls = [i for ind, item in enumerate(urls) if ind not in shouldIgnores for i in item]

        indexes = input("请输入您想下载的歌曲版本(填序号,多个用英文逗号隔开):").split(',')

        if not hasattr(Constants, 'savePath'):
            savePath = input("请输入保存路径(空则为脚本所在路径):")
        else:
            savePath = None

        if savePath:
            if not os.path.exists(savePath):
                raise PathNotExistsError('不存在的路径')
            download = self.download(path=savePath)
        else:
            download = self.download(path=Constants.defaultSavePath)

        for i in indexes:
            i = int(i) - 1
            download(urls[i], authors[i], titles[i])


if __name__ == '__main__':
    import sys

    args = {
        key: value
        for item in sys.argv[1:]
        for key, value in [item.split('=')]
    }
    if '--path' in args:
        Constants.savePath = args['--path']
    Crawler().main()