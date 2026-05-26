import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from pydantic import ValidationError
from starlette.responses import JSONResponse

from model.res import StdErrorRes
from model.error import StdError, ErrorCode

from lib.configure import Configure
from lib.logging import LoggingHelper, logger
from lib.mysql import MysqlHelper

Configure.read_yaml("./config.yaml")

from controller import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 项目启动
    LoggingHelper.init()  # 配置日志器
    await MysqlHelper.init()  # 创建数据库连接

    yield

    # 项目关闭
    await MysqlHelper.dispose()


app = FastAPI(routes=router.routes, lifespan=lifespan)


# 错误拦截（参数校验失败）
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # 从异常中提取错误消息
    logger.error(f"{request.url.path} request failed: {exc}")
    return JSONResponse(
        status_code=200,
        content=StdErrorRes.create(
            ErrorCode.ParamsError.value[0], exc.__str__()
        ).model_dump(),
    )


# 错误拦截（自定义错误）
@app.exception_handler(StdError)
async def base_exception_handler(request: Request, exc: StdError):
    logger.error(f"{request.url.path} request failed: {exc}")
    return JSONResponse(
        status_code=200,
        content=StdErrorRes.create(exc.code, exc.msg).model_dump(),
    )


# 错误拦截（全局异常）
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f"{request.url.path} request failed: {exc}")
    return JSONResponse(
        status_code=200,
        content=StdErrorRes.create(*ErrorCode.UnexpectedError.value).model_dump(),
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=Configure.get("app", "host"),
        port=Configure.get("app", "port"),
    )
