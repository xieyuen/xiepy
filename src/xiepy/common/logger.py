import datetime
import logging
import re
import zipfile
from pathlib import Path
from typing import Optional

import colorlog


class CustomColoredFormatter(colorlog.ColoredFormatter):
    """
    自定义颜色格式化器，支持毫秒级时间戳（%f）。
    控制台时间格式不含毫秒，文件日志含毫秒，通过 datefmt 区分。
    """

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """
        重写 formatTime 以支持 %f 占位符（毫秒，三位）。
        """
        if datefmt is None:
            datefmt = self.datefmt
        if datefmt and "%f" in datefmt:
            # 先按去掉 %f 的格式格式化
            base_fmt = datefmt.replace("%f", "")
            dt = datetime.datetime.fromtimestamp(record.created)
            base_str = dt.strftime(base_fmt)
            millis = int(record.msecs)  # 毫秒整数
            return base_str + f"{millis:03d}"
        # 其他情况调用父类默认实现
        return super().formatTime(record, datefmt)


def archive_old_log(log_path: str | Path) -> None:
    """
    将现有的 logs/xiepy.log 压缩为 program-{date}-{times}.zip，
    并删除原日志文件。times 根据当天已有 zip 文件数量自动递增。
    """
    log_path = Path(log_path)
    if not log_path.exists():
        return

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    pattern = re.compile(rf"^program-{date_str}-(\d+)\.zip$")
    max_times = 0
    parent = log_path.parent
    parent.mkdir(exist_ok=True)

    for f in parent.glob("*.zip"):
        match = pattern.match(f.name)
        if match:
            times = int(match.group(1))
            if times > max_times:
                max_times = times

    new_times = max_times + 1
    zip_name = f"program-{date_str}-{new_times}.zip"
    zip_path = parent / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(log_path, arcname="xiepy.log")

    # 压缩成功后删除原日志
    log_path.unlink()


def get_logger(
        name: Optional[str] = None,
        enable_file: bool = True,
        level: int | str = logging.INFO,
) -> logging.Logger:
    """
    创建一个配置好的 Logger 实例。

    :param name: Logger 名称，通常传入 __name__，为 None 时返回根 Logger。
    :param enable_file: 是否启用文件输出。若为 True，则输出到 logs/xiepy.log 并自动归档旧文件。
    :param level: 日志级别，可为 int（如 logging.INFO）或字符串（如 "INFO"）。
    :return: 配置完成的 Logger 对象。
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 清除已有 handlers，避免重复添加
    if logger.handlers:
        logger.handlers.clear()

    # ---------- 控制台 Handler（带颜色） ----------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    console_format = (
        "[%(asctime)s] [%(threadName)s/%(log_color)s%(levelname)s%(reset)s] "
        "[%(filename)s(%(funcName)s:%(lineno)d)]: %(message)s"
    )
    console_formatter = CustomColoredFormatter(
        console_format,
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # ---------- 文件 Handler ----------
    if enable_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_path = log_dir / "xiepy.log"

        # 若已存在旧日志，先压缩归档
        if log_path.exists():
            archive_old_log(log_path)

        file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        file_handler.setLevel(level)

        file_format = (
            "[%(asctime)s] [%(threadName)s/%(levelname)s] "
            "[%(filename)s(%(funcName)s:%(lineno)d)]: %(message)s"
        )
        file_formatter = CustomColoredFormatter(
            file_format,
            datefmt="%Y-%m-%d %H:%M:%S.%f",
            reset=False,  # 文件无需颜色
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
