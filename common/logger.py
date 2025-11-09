import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timezone

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def _get_logger():
    logger = logging.getLogger("project_TestWebUI")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    # 使用时区感知的 UTC 时间
    log_file = os.path.join(LOG_DIR, f"{datetime.now(timezone.utc).strftime('%Y%m%d')}.log")

    handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7, utc=True, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

log = _get_logger()