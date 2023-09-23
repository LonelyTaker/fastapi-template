import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from lib.logging_helper import LoggingHelper
from lib.mysql_helper import MysqlHelper

from controller import router
from model import BaseError, ErrorCode
from setting import SERVICE_IP, SERVICE_PORT

app = FastAPI(routes=router.routes)
logger = logging.getLogger()


# 错误拦截（参数校验失败）
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # 从异常中提取错误消息
    errors = exc.errors()
    error_msgs = [error["msg"] for error in errors]
    error_response = "; ".join(error_msgs)
    logger.error(f'{request.url.path} request failed: {error_response}')
    return JSONResponse(status_code=200,
                        content={"code": ErrorCode.ParamsError.value[0], "msg": error_response, "data": None})


# 错误拦截（自定义错误）
@app.exception_handler(BaseError)
async def base_exception_handler(request: Request, exc: BaseError):
    logger.error(f'{request.url.path} request failed: {exc}')
    return JSONResponse(status_code=200, content={"code": exc.code, "msg": exc.msg, "data": None})


# 错误拦截（全局异常）
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f'{request.url.path} request failed: {exc}')
    return JSONResponse(status_code=200,
                        content={"code": ErrorCode.UnexpectedError.value[0], "msg": ErrorCode.UnexpectedError.value[1],
                                 "data": None})


# 项目启动
@app.on_event(r'startup')
async def startup_event():
    # 配置日志器
    LoggingHelper.init()
    # 创建数据库连接
    MysqlHelper.init()


# 项目关闭
@app.on_event(r'shutdown')
async def shutdown_event():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host=SERVICE_IP, port=SERVICE_PORT)
