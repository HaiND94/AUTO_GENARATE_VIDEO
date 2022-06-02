"""""""""""""""""""""""
Author : NGUYEN DINH HAI
VER    : 1.0
DATE   : 2021, JUL 12
"""""""""""""""""""""""

from datetime import datetime, date

import getpass
import os
import sys
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


def log(url, msg):
    logging.info(msg)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    today_str = today.strftime("%d/%m/%Y")
    user = getpass.getuser()
    msg_write = f'{today_str} - {current_time} - {user}: {msg}\n'
    with open(url, 'a') as f:
        f.write(msg_write)
        f.close()

