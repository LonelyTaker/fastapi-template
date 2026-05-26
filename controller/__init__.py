from fastapi import APIRouter

from lib.configure import Configure

from . import user_controller, account_controller

_name = Configure.get("app", "name")
_version = Configure.get("app", "version")

# 接口公共前缀
router = APIRouter(prefix=f"/{_name}/{_version}")

# 各功能模块接口
router.include_router(user_controller.router)
router.include_router(account_controller.router)
