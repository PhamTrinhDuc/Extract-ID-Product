import logging
import datetime
import os


def set_logging_error():
    logger = logging.getLogger("file")
    logger.setLevel(logging.DEBUG)

    folder_path = os.path.join("logs", "error")
    os.makedirs(folder_path, exist_ok=True)
    today = datetime.date.today()
    log_filename = today.strftime('%Y-%m-%d') + '-logging.txt'  # Định dạng: YYYY-MM-DD.log

    file_handler = logging.FileHandler(os.path.join(folder_path, log_filename), mode='a') # mode a: apppend, mode w: ghi đè
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def set_logging_file():
    logger = logging.getLogger("error")
    logger.setLevel(logging.DEBUG)

    folder_path = os.path.join("logs", "file")
    os.makedirs(folder_path, exist_ok=True)
    today = datetime.date.today()
    log_filename = today.strftime('%Y-%m-%d') + '-logging.txt'  # Định dạng: YYYY-MM-DD.log

    file_handler = logging.FileHandler(os.path.join(folder_path, log_filename), mode='a') # mode a: apppend, mode w: ghi đè
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger