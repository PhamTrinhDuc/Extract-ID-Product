from ftplib import FTP
import os
import pandas as pd
import datetime
import run_threas
from logs.set_logging import set_logging_file
logger_file = set_logging_file() # sử dụng để ghi log các file đã xử lí 


# Thông tin kết nối FTP
ftp_server = "10.61.19.198"
ftp_user = "ctct"
ftp_password = "ctct123"
ftp_directory = "/RPA/RPA_ads/"

# Kết nối đến server FTP
ftp = FTP(ftp_server)
ftp.login(user=ftp_user, passwd=ftp_password)
# Đổi thư mục đến thư mục chứa file
ftp.cwd(ftp_directory)
# Lấy danh sách các file trong thư mục
files = ftp.nlst()


# File lưu trữ tên các file đã xử lý
today = datetime.date.today()
log_filename = today.strftime('%Y-%m-%d') + '-processed_file.txt'
log_filename = os.path.join("logs", "file", log_filename)

# Hàm kiểm tra file đã xử lý hay chưa
def is_processed(filename):
    with open(log_filename, "r") as f:
        processed_files = f.read().splitlines()
    for processed_file in processed_files:
        if filename in processed_file:
            return True
    return False

# thư mục lưu file download
data_dir = "data"

list_file_name = []
for idx, file in enumerate(files, start=1):
    if file.endswith(".xlsx") or file.endswith(".xls"):
        if not is_processed(file):
            logger_file.info(file) # Đánh dấu file là đã xử lý
            local_filename = os.path.join(data_dir, file)
            with open(local_filename, "wb") as local_file:
                ftp.retrbinary(f"RETR {file}", local_file.write)
            
            list_file_name.append(local_filename)

            if len(list_file_name) == 10: # chạy 10 file 1 lần
                run_threas.run(list_file_name)
                list_file_name = []

# Đóng kết nối
ftp.quit()