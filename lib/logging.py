import json
import time
import sys
from functools import wraps
from loguru import logger

from lib.configure import Configure


class LoggingHelper:
    _initialized = False

    @classmethod
    def init(cls):
        if cls._initialized:
            return

        folder_ = Configure.get("log", "path", default="./logs/")
        prefix_ = Configure.get("log", "prefix", default="")
        rotation_ = "10 MB"
        retention_ = "30 days"
        encoding_ = "utf-8"
        backtrace_ = True
        diagnose_ = True

        # 格式里面添加了process和thread记录，方便查看多进程和线程程序
        format_ = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> "
            "| <magenta>{process}</magenta>:<yellow>{thread}</yellow> "
            "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>"
        )

        # 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
        # debug
        # logger.add(
        #     folder_ + prefix_ + "debug.log",
        #     level="DEBUG",
        #     backtrace=backtrace_,
        #     diagnose=diagnose_,
        #     format=format_,
        #     colorize=False,
        #     rotation=rotation_,
        #     retention=retention_,
        #     encoding=encoding_,
        #     filter=lambda record: record["level"].no >= logger.level("DEBUG").no,
        # )

        # info
        logger.add(
            folder_ + prefix_ + "info.log",
            level="INFO",
            backtrace=backtrace_,
            diagnose=diagnose_,
            format=format_,
            colorize=False,
            rotation=rotation_,
            retention=retention_,
            encoding=encoding_,
            filter=lambda record: record["level"].no >= logger.level("INFO").no,
        )

        # warning
        logger.add(
            folder_ + prefix_ + "warning.log",
            level="WARNING",
            backtrace=backtrace_,
            diagnose=diagnose_,
            format=format_,
            colorize=False,
            rotation=rotation_,
            retention=retention_,
            encoding=encoding_,
            filter=lambda record: record["level"].no >= logger.level("WARNING").no,
        )

        # error
        logger.add(
            folder_ + prefix_ + "error.log",
            level="ERROR",
            backtrace=backtrace_,
            diagnose=diagnose_,
            format=format_,
            colorize=False,
            rotation=rotation_,
            retention=retention_,
            encoding=encoding_,
            filter=lambda record: record["level"].no >= logger.level("ERROR").no,
        )

        # critical
        logger.add(
            folder_ + prefix_ + "critical.log",
            level="CRITICAL",
            backtrace=backtrace_,
            diagnose=diagnose_,
            format=format_,
            colorize=False,
            rotation=rotation_,
            retention=retention_,
            encoding=encoding_,
            filter=lambda record: record["level"].no >= logger.level("CRITICAL").no,
        )

        logger.add(
            sys.stderr,
            level="CRITICAL",
            backtrace=backtrace_,
            diagnose=diagnose_,
            format=format_,
            colorize=True,
            filter=lambda record: record["level"].no >= logger.level("CRITICAL").no,
        )

        cls._initialized = True

    @classmethod
    def log_request(cls, func):
        @wraps(func)
        async def inner(request, *args, **kwargs):
            start_time = time.time()
            content_type = request.headers.get("content-type")

            if isinstance(content_type, str) and content_type.startswith(
                "application/json"
            ):
                params = await request.body()
                logger.info(f"{request.url.path} request params: {json.loads(params)}")
            elif isinstance(content_type, str) and content_type.startswith(
                "multipart/form-data"
            ):
                logger.info(f"{request.url.path} request params: form-data")
            else:
                logger.info(f"{request.url.path} request params: unknown")

            data = await func(request, *args, **kwargs)
            logger.info(f"{request.url.path} response: {data}")

            process_time = (time.time() - start_time) * 1000
            logger.info(f"{request.url.path} request runtime: {process_time:.2f}ms")

            return data

        return inner
