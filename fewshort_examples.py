
examples_prompt = [ # create example to fewshort
        {
            "command":"máy giặt aqua fr110gt",
            "ID" : "fr110gt",
        },
        {
            "command":"máy giặt lg 9 kg fm1209n6w",
            "ID":"fm1209n6w",
        },
        {
            "command":"máy giặt lg chợ tốt",
            "ID":"None",
        },
        {
            "command":"máy giặt electrolux 10kg",
            "ID":"None",
        },
        {
            "command":"máy giặt lg inverter 9 kg fm1209s6w",
            "ID":"fm1209s6w",
        },
         {
            "command": "máy giặt samsung inverter 8kg ww80t3020ww sv",
            "ID": "ww80t3020ww",
        },
        {
            "command": "máy giặt sấy lg inverter 9 kg fv1409g4v",
            "ID": "fv1409g4v",
        },
        {
            "command":"điện máy chợ lớn máy giặt",
            "ID":"None",
        },
        {
            "command":"máy giặt lg inverter 10 kg fv1410s3b",
            "ID":"fv1410s3b",
        },
        {
            "command":"máy giặt sấy samsung wd95t754dbx sv",
            "ID":"wd95t754dbx",
        },
        {
            "command":"máy giặt lg fv1410s3b",
            "ID":"fv1410s3b",
        },
        {
            "command":"máy giặt dưới 3 triệu điện máy xanh",
            "ID":"None",
        },
        {
            "command":"máy giặt sấy samsung inverter 9.5 kg wd95t4046ce sv",
            "ID":"wd95t4046ce",
        },
        {
            "command":"máy giặt sấy samsung addwash inverter 9.5 kg wd95t754dbx sv",
            "ID":"wd95t754dbx",
        },
        {
            "command":"máy giặt casper 9.5 kg",
            "ID":"None",
        },
        {
            "command":"máy giặt và sấy",
            "ID":"None",
        },
        {
            "command":"máy giặt lg fv1408s4w",
            "ID":"fv1408s4w",
        },
        {
            "command": "aw uk1150hv sg",
            "ID": "uk1150hv"
        },
        {
            "command": "dc68 02590j 04",
            "ID": "02590j"
        },
        {
            "command": "máy giặt aqua aqw u100ft bk",
            "ID": "u100ft"
        },
    ]


import logging
import os
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


os.makedirs("./logs", exist_ok=True)
today = datetime.date.today()
log_filename = today.strftime('%Y-%m-%d') + '-logging.txt'  # Định dạng: YYYY-MM-DD.log


file_handler = logging.FileHandler("./logs/" + log_filename, mode='a') # mode a: apppend, mode w: ghi đè
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


logger.debug("Bắt đầu chương trình")
