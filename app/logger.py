
import logging
from logging.handlers import RotatingFileHandler

# Создание обработчика с ротацией файлов
handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=3)  # 1MB, храним 3 файла

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("rotating_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
