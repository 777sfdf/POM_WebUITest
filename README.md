# Selenium + pytest + POM + YAML + Logger + Allure Demo

This demo shows a layered POM-style test project using:
- Python 3.12
- selenium==4.37.0
- pytest
- allure-pytest==2.18.1
- yaml for configuration
- custom logger
- webdriver-manager to manage chromedriver

Project structure
```
.
├── config
│   └── config.yaml
├── pages
│   ├── base_page.py
│   ├── login_page.py
│   └── secure_page.py
├── tests
│   └── test_login.py
├── utils
│   ├── logger.py
│   ├── yaml_utils.py
│   └── helpers.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

Quickstart
1. Create a venv with Python 3.12
2. pip install -r requirements.txt
3. Run tests and write allure results:
   pytest -q --alluredir=allure-results
4. View allure report (requires Allure CLI):
   - Install Allure CLI (https://docs.qameta.io/allure/)
   - Serve report:
     allure serve allure-results

Notes
- Tests use https://the-internet.herokuapp.com/login as demo site.
- Update config/config.yaml if you want headless mode or different browser.
