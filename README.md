# WebUI 自动化测试项目

## 项目简介

基于 Python + Selenium + Pytest 的 WebUI 自动化测试框架，采用 POM（Page Object Model）设计模式，支持数据驱动测试和 Allure 测试报告生成。

## 技术栈

- **编程语言**: Python 3.12
- **自动化框架**: Selenium 4.37.0
- **测试框架**: Pytest
- **数据管理**: YAML
- **日志管理**: Logger
- **测试报告**: Allure 2.18.1

## 环境要求

- Python 3.12
- Allure 2.18.1
- 配置环境变量

## 项目结构
```
POM_WebUITest/
├── common/                      # 通用工具类
│   ├── __init__.py
│   ├── config_utils.py         # 配置工具
│   ├── logger.py               # 日志工具
│   └── screenshot.py           # 截图工具
├── config/                     # 配置文件目录
│   ├── __init__.py
│   ├── config.ini             # 主配置文件
│   └── environment.yaml       # 环境配置
├── data/                       # 测试数据目录
│   ├── account/               # 账号模块数据
│   │   ├── login.yaml
│   │   ├── register.yaml
│   │   └── orders.yaml
│   ├── admin/                 # 管理模块数据
│   ├── cart/                  # 购物车数据
│   ├── catalog/               # 商品目录数据
│   ├── checkout/              # 结算数据
│   ├── payment/               # 支付数据
│   └── __init__.py
├── drivers/                    # 浏览器驱动目录
│   ├── __init__.py
│   ├── chromedriver.exe       # Chrome驱动
│   └── msedgedriver.exe       # Edge驱动
├── logs/                       # 日志文件目录
├── originalpages/              # 原型页面和主流程
│   ├── __init__.py
│   ├── loginDiffCase.py       # 登录反例场景测试
│   └── masterFlow.py          # 主流程测试
├── pageobjects/                # 页面对象模型目录
│   ├── base/
│   │   └── base_page.py       # 页面基类
│   └── account/
│       ├── login_page.py      # 登录页面
│       └── register_page.py   # 注册页面
├── reports/                    # 测试报告目录
├── testcases/                  # 测试用例目录
├── utils/                      # 工具类目录
│   └── __init__.py
├── conftest.py                # pytest配置文件
├── pytest.ini                 # pytest配置
├── README.md                  # 项目说明文档
├── requirements.txt           # 项目依赖包
├── run.py                     # 项目运行入口
└── stop_allure.py             # 停止allure服务脚本
```



## 快速开始

### 1. 环境安装

```bash
# 安装项目依赖
pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 原型页面测试

1. 打开原型页面脚本，修改用户名和密码
`originalpages/masterFlow.py`  这个脚本就是原型页面测试的脚本
2. 启动项目数据库
3. 运行原型测试：
   ```bash
   python ./originalpages/masterFlow.py
   ```

### 3. 冒烟测试
0.修改 `config/environment.yaml` 文件中的dev环境用户名和密码
1. 修改 `data/account/login.yaml` 文件中的用户名和密码
2. 运行冒烟测试：
   ```bash
   pytest -m "smoke" -q --alluredir=reports/allure-results
   ```
3. 生成测试报告：
   ```bash
   allure serve reports/allure-results
   ```
4. 停止服务：按 `Ctrl+C` 然后输入 `y`
5. 如果上边都测试完毕了 想使用一条命令解决自动测试 自动生成报告可以在控制台使用如下命令:
   ```bash
   python run.py --serve --background
   ```

## 使用指南

### 添加新模块

1. **页面对象**: 在 `pageobjects/` 下创建对应模块的页面类
2. **测试用例**: 在 `testcases/` 下编写测试用例
3. **测试数据**: 在 `data/` 下添加对应的 YAML 数据文件

参考示例：
- 页面对象: `pageobjects/account/login_page.py`
- 测试用例: `testcases/account/test_login.py`
- 测试数据: `data/account/login.yaml`




### 日志查看

测试运行日志保存在 `logs/` 目录下，按日期生成日志文件。


## 注意事项

1. 确保浏览器驱动与浏览器版本匹配
2. 测试数据文件使用 UTF-8 编码
3. 运行前检查环境变量配置
4. Allure 报告需要提前安装 Allure 命令行工具



### 常见问题
1. **驱动找不到**: 检查 drivers 目录或配置环境变量
2. **元素定位失败**: 检查页面加载时间和元素定位策略
3. **报告生成失败**: 确认 Allure 已正确安装并配置环境变量

