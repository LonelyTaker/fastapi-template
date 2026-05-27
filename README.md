# fastapi-template

## 介绍
fastapi项目简易模板

<br />

## 目录结构

```tex
├── controller                         controller控制层
│    ├── account_controller.py
│    ├── user_controller.py
│    └── ...
├── db                                 sql脚本存放目录
│    ├── 1.0.0                         按版本号归档
│    │    └── user.sql
│    └── ...
├── lib                                相关辅助/工具类
│    ├── configure.py                  配置加载类
│    ├── logging.py                    日志配置类
│    ├── mysql.py                      mysql辅助类
│    └── ...
├── logs                               日志存放目录
│    └── ...
├── model                              model实体层
│    ├── base                          基础模块
│    │    ├── error.py                 自定义异常相关
│    │    └── res.py                   统一响应模型
│    ├── schema                        请求/响应模型
│    │    ├── account.py
│    │    ├── user.py
│    │    └── ...
│    ├── table                         ORM表模型
│    │    ├── account.py
│    │    ├── user.py
│    │    └── ...
│    └── ...
├── service                            service业务服务层
│    ├── auth_service.py
│    └── ...
├── sql                                dao数据访问层
│    ├── account_dao.py
│    ├── user_dao.py
│    └── ...
├── utils                              常用工具函数
│    └── ...
├── .gitignore                         git忽略文件
├── config.yaml                        配置文件
├── docker-compose.yml                 docker-compose配置
├── Dockerfile                         docker镜像构建文件
├── main.py                            入口文件
├── README.md                          项目说明
└── requirements.txt                   项目依赖说明
```

项目中`user`、`account`相关内容为示例代码，进行开发时请删除

<br />

## 启动项目

### 虚拟环境启动

#### 1.安装依赖

```python
pip install -r requirements.txt
```

#### 2.运行项目

```python
python main.py
# 后台运行
nohup python main.py > /dev/null 2>&1 &
```

<br />

### docker启动

项目目录：`/data/container/fastapi-template`

#### 1.构建镜像

```shell
docker build -t fastapi-template:latest .
```

注意最后的点（当前文件夹）

#### 2.docker-compose运行

```shell
docker-compose up
# 后台运行
docker-compose up -d
```

