import logging
import json
import time
from logging.handlers import TimedRotatingFileHandler
from functools import wraps
from fastapi import Request

from setting import LOGS_PATH, SERVICE_NAME


# 日志辅助类
class LoggingHelper(object):
    __logger = logging.getLogger()

    @classmethod
    def init(cls):
        # 日志等级
        logging_level = logging.INFO
        # 格式化
        logging_fmt_str = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(name)s - %(levelname)s: %(message)s'
        logging_fmt = logging.Formatter(logging_fmt_str)
        # 创建处理器
        logging_handler = TimedRotatingFileHandler(f'{LOGS_PATH}/{SERVICE_NAME}.log', when='midnight', interval=1, backupCount=30, encoding="utf-8")
        logging_handler.suffix = '%Y-%m-%d'
        logging_handler.setFormatter(logging_fmt)

        # 初始化logging
        logging.basicConfig(level=logging_level)
        # 将处理器添加到全局logger
        cls.__logger.addHandler(logging_handler)

    # 请求日志打印装饰器
    @classmethod
    def log_request(cls, func):
        @wraps(func)
        async def inner(request: Request, *args, **kwargs):
            start_time = time.time()
            content_type = request.headers.get('content-type')
            if isinstance(content_type, str) and content_type.startswith('application/json'):
                params = await request.body()
                cls.__logger.info(f"{request.url.path} request params: {json.loads(params)}")
            elif isinstance(content_type, str) and content_type.startswith('multipart/form-data'):
                cls.__logger.info(f"{request.url.path} request params: form-data")
            else:
                cls.__logger.info(f"{request.url.path} request params: unknown")
            data = await func(request, *args, **kwargs)
            cls.__logger.info(f"{request.url.path} response: {data}")
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = '{0:.2f}'.format(process_time)
            cls.__logger.info(f'{request.url.path} request runtime: {formatted_process_time}ms')
            return data

        return inner
