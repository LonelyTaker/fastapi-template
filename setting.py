"""
    项目的配置文件
    1.请根据实际情况修改服务名称、服务版本、服务IP、端口号等相关配置
    2.如果项目接入nacos，所有 中间件 的配置信息应使用nacos的配置管理，不再在该文件中配置
"""

# 服务名称
SERVICE_NAME = "example-service"
# 服务版本
SERVICE_VERSION = 'v1'
# 服务IP
SERVICE_IP = "0.0.0.0"
# 服务端口
SERVICE_PORT = 7866

# 日志路径
LOGS_PATH = "./logs"

# nacos配置
# NACOS_INFO = {
#     # 多host使用逗号分割
#     'host': '',
#     'namespace': '',
#     'data_id': '',
#     'group': ''
# }

# mysql配置
MYSQL_INFO = {
    # 连接地址
    'url': "mysql+aiomysql://[用户名]:[密码]@[IP]:[端口号]/[数据库名]?charset=utf8mb4",
    # 超过链接池大小外最多创建的链接
    'max_overflow': 0,
    # 链接池大小
    'pool_size': 50,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    'pool_timeout': 10,
    # 多久之后对链接池中的链接进行一次回收
    'pool_recycle': 1,
    # 查看原生语句（调试用）
    'echo': False,
    # 查看链接池（调试用）
    'echo_pool': False
}
