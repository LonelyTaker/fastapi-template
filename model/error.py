import json
from enum import Enum, unique


# 自定义错误类型
class BaseError(Exception):
    def __init__(self, code: int, msg: str, scene: str):
        self.code = code
        self.msg = msg
        self.scene = scene

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


# 自定义错误码
@unique
class ErrorCode(Enum):
    # 通用错误码
    Ok = (0, "ok")
    UnexpectedError = (-1, "系统异常")
    ConfigError = (1000, "配置错误")
    ParamsError = (1001, "参数错误")
    ServiceError = (1002, "服务异常")  # 服务不可用，或请求下游服务异常
    LockError = (1099, "系统繁忙")  # 未抢占到锁
    # 项目特殊错误码
    UserAddError = (1101, "用户创建失败")
    UserDelError = (1102, "用户删除失败")
    UserUpdateError = (1103, "用户信息更新失败")
    UserListError = (1104, "查询用户列表失败")
