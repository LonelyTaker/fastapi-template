# fastapi-template

## 介绍
fastapi项目简易模板

<br />

## 目录结构

```tex
├── controller                            controller控制层
│    ├── user_controller
│    └── ...
├── db                                    sql脚本存放目录
│    ├── 1.0.0                            按版本号归档
│    │    └── user.py
│    └── ...
├── lib                                   相关辅助/工具类
│    ├── logging_helper.py                日志配置类
│    ├── mysql_helper.py                  mysql辅助类
│    └── utils.py                         常用函数
├── logs                                  日志存放目录
│    └── ...
├── model                                 model实体层
│    ├── base.py                          ORM基础类/业务基础类
│    ├── error.py                         自定义异常相关
│    ├── user.py
│    └── ...
├── service                               service业务服务层
│    └── ...
├── sql                                   dao数据访问层
│    ├── user_dao.py
│    └── ...
├── .gitignore                            git忽略文件
├── main.py                               入口文件
├── README.md                             项目说明
├── requirements.py                       项目依赖说明
└── setting.py                            配置文件
```

项目中`user`、`account`相关内容为示例代码，进行开发时请删除

<br />

## 启动项目

### 1.安装依赖

```python
pip install -r requirements.txt
```

### 2.运行项目

```python
python main.py
```

<br />

