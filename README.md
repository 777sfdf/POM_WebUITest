# POM Web UI Test Demo

这是一个基于 POM（Page Object Model）分层设计的 Web UI 自动化工程示例，演示如何组织测试用例、页面对象、公共工具、配置与数据分离。

主要技术栈：
- Python 3.12
- selenium==4.37.0
- pytest
- allure-pytest==2.18.1
- PyYAML
- webdriver-manager

项目结构示例
```
project_name/
├── testcases/                 # 测试用例层（核心业务场景）
│   ├── __init__.py
│   ├── test_login.py
│   └── test_order.py
├── pageobjects/               # 页面对象层
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── order_page.py
├── common/                    # 公共工具层
│   ├── __init__.py
│   ├── logger.py
│   ├── config_utils.py
│   ├── screenshot.py
│   └── send_email.py
├── config/
│   ├── __init__.py
│   ├── config.ini
│   └── environment.yaml
├── data/
│   ├── __init__.py
│   ├── login_data.json
│   └── order_data.json
├── drivers/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── conftest.py
├── run.py
├── requirements.txt
└── README.md
```

Quickstart 与运行同之前说明，详见仓库内 README。
