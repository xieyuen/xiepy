from xiepy.common.exceptions import DependencyNotInstalled

try:
    import mcdreforged

    del mcdreforged
except ModuleNotFoundError:
    raise DependencyNotInstalled(
        "此模块需要 MCDReforged, 请先安装依赖: pip install -U mcdreforged",
    )
