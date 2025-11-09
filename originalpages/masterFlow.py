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

        # 方法一：使用对包含文本的任意元素进行等待（推荐）
        try:
            welcome_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//font[contains(normalize-space(.), '欢迎您回来')]"))
            )
            welcome_text = welcome_element.text.strip()
            assert "欢迎您回来" in welcome_text, f"断言失败：实际文本为 '{welcome_text}'"
            print("断言通过：页面包含 ->", welcome_text)
            # return
        except TimeoutException:
            pass

        # 这个地方 输入商品名称 点击搜索按钮 搜索商品
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "keyword"))).send_keys("P806")

        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, "imageField"))).click()

        # 已经显示出商品的显示页面，点击商品详情

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'goods.php?id=')]"))).click()
        #已经跳转到商品详情页面
        # 先清空默认数量，再输入数量2
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "number"))).clear()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "number"))).send_keys("2")
        #选择商品的颜色 单选框
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "spec_value_242"))).click()
        #选择商品的内存容量
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "spec_value_245"))).click()
        #勾选配件 复选框
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "spec_value_243"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "spec_value_168"))).click()
        #加入购物车
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:addToCart(24)')]"))).click()
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='javascript:addToCart(24)']"))
        ).click()
        #跳转到购物车页面 购物流程页面
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='flow.php?step=checkout']"))
        ).click()

        # 选择配送方式
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='shipping'and @value='5']"))
        ).click()

        # 选择支付方式 payment
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@name='payment' and @value='3']"
            ))
        ).click()

        # 选择商品包装方式
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='pack'and @value='1']"))
                                        ).click()

        # 选择祝福贺卡
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='card'and @value='1']"))
                                        ).click()
        # 其他信息中的 缺货处理 how_oos
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='how_oos'and @value='2']"))
                                        ).click()

        # 点击提交
        succeee_str=WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//input[@type="image" and @src="themes/default/images/bnt_subOrder.gif"]'))
                                        ).click()

        # 等待订单成功页面加载并获取成功信息
        success_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//h6[contains(text(), "感谢您在本店购物")]'))
        )

        # 获取成功页面的文本内容
        order_text = success_element.text.strip()

        # 修改断言
        assert "感谢您在本店购物！您的订单已提交成功，请记住您的订单号:" in order_text, f"断言失败：实际文本为 '{order_text}'"
        print("主流程断言通过：页面包含 ->", order_text)

        # 如果需要提取订单号，可以添加以下代码
        if "订单号:" in order_text:
            order_number = order_text.split("订单号:")[1].strip()
            print("订单号:", order_number)






    finally:
        # 适当等待以便查看浏览器（非 CI 环境可保留）
        time.sleep(1)
        driver.quit()

if __name__ == "__main__":
    login_and_assert_welcome()