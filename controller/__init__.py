from fastapi import APIRouter
from setting import SERVICE_NAME, SERVICE_VERSION

from controller import user_controller

# 接口公共前缀
router = APIRouter(prefix=f'/{SERVICE_NAME}/{SERVICE_VERSION}')

# 各功能模块接口
router.include_router(user_controller.router)
