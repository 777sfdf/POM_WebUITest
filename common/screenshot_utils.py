import allure

def attach_fullscreen(name: str = "全屏_含地址栏_截图"):
    """
    使用操作系统级截图（mss）捕获整个屏幕，确保包含浏览器地址栏等浏览器外壳。
    注意：
    - 需在非 headless 模式下运行
    - 浏览器窗口请确保在最前台且未被遮挡
    """
    try:
        import mss
        from mss import tools
    except Exception:
        # 兜底：若 mss 未安装或不可用，退回页面区域截图（不含地址栏）
        try:
            allure.attach(
                b"",  # 空图占位，避免抛错
                name=f"{name}_mss_not_available",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass
        return

    try:
        with mss.mss() as sct:
            # 取主显示器；如有多显示器可选择 monitors[1] 以外的索引
            monitor = sct.monitors[1]
            shot = sct.grab(monitor)
            png = tools.to_png(shot.rgb, shot.size)
            allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
    except Exception:
        # 兜底：失败则不阻断用例
        try:
            allure.attach(
                b"",
                name=f"{name}_screenshot_failed",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass