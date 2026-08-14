import threading

from xiepy.common.logger import get_logger


def worker():
    """多线程测试"""
    t_log = get_logger("worker", enable_file=False)  # 子线程只输出到控制台
    t_log.info("Worker thread running")


def main():
    log = get_logger(__name__)
    log.debug("Debug message")
    log.info("Hello World")
    log.warning("This is a warning")
    log.error("Something went wrong")
    log.critical("Critical error occurred")
    t = threading.Thread(target=worker, name="WorkerThread")
    t.start()
    t.join()


if __name__ == "__main__":
    main()
