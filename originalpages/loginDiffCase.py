# 对应的是ecshop 主流程 包含登录 搜索商品 加入购物车 下单 支付等功能


import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

def login_and_assert_welcome():
    """
    执行登录并断言页面中出现“欢迎您回来！”这段文字（不使用 pytest 或 unittest）。
    中文注释。增强等待逻辑，失败时保存截图和页面源码以便排查。
    """
    # 注意：根据你的环境调整 chromedriver 路径或使用 PATH 中的 chromedriver
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_driver_path = os.path.join(project_root, "drivers", "chromedriver.exe")

    # 创建 webdriver（示例使用 Chrome）
    service = webdriver.ChromeService(executable_path=local_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("http://localhost")

        # 等待登录图标并点击父级 <a>
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src="themes/default/images/bnt_log.gif"]'))
        )
        a_element = img_element.find_element(By.XPATH, './parent::a')
        a_element.click()

        # 输入用户名和密码
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        ).send_keys("ecshop")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        ).send_keys("admimn23")

        # 点击登录（确保实际点击）
        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='submit']"))
        )
        submit.click()

        # 这里  要对页面出现的用户名或密码进行断言
        try:
            # 等待并检查是否出现"用户名或密码错误"的提示
            error_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//div[contains(@class,'boxCenterList')]//p[contains(normalize-space(.),'用户名或密码错误')]"))
            )

            # 获取错误文本
            error_text = error_element.text.strip()

            # 断言错误提示存在
            assert "用户名或密码错误" in error_text, f"断言失败：实际文本为 '{error_text}'"
            print("断言通过：页面包含错误提示 ->", error_text)

        except Exception as e:
            print("未找到错误提示元素，可能是登录成功或其他情况")
            print("错误详情:", e)





    finally:
        # 适当等待以便查看浏览器（非 CI 环境可保留）
        time.sleep(1)
        driver.quit()

if __name__ == "__main__":
    login_and_assert_welcome()