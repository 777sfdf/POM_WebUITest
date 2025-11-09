import os
from datetime import datetime

def take_screenshot(driver, name="screenshot"):
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports", "screenshots")
    logs_dir = os.path.abspath(logs_dir)
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(logs_dir, filename)
    driver.save_screenshot(path)
    return path