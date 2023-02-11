"""
Modified: 02/10,
devkim1102@gmail.com
"""

import os
import pickle
import random
import subprocess
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bot_utils import driver_sleep, get_latest_article_num, message_scheduler, band_info_parsing, kakao_send

import config as cfg

if __name__ == '__main__':
    chrome_path = cfg.chrome_path
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", cfg.chrome_address)

    chrome_explorer = subprocess.Popen(chrome_path)
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    time.sleep(10)
    current_hour, prev_day = 0, 0

    # create kakao_log file
    if not os.path.isfile(os.path.isfile(cfg.kakao_log)):
        with open(file=cfg.kakao_log, mode='wb') as f:
            pickle.dump({}, f)

    # pyautogui.click(x=cfg.m_position0[1], y=cfg.m_position0[1])  # kakao

    while True:
        task_todo = message_scheduler()
        if not task_todo:
            time.sleep(random.randint(120, 300))
            continue

        with open(file=cfg.kakao_log, mode='rb') as f:
            kakao_log = pickle.load(f)

        while True:
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            try:
                # get to rebhub auction bulletin
                if not today == prev_day:
                    today_article_num = get_latest_article_num(driver, cfg.rebhub_address + cfg.rebhub_auction)
                driver.get(cfg.rebhub_address + '/' + today_article_num)
                driver_sleep(driver, 2, 3)
                driver.switch_to.frame("cafe_main")
                contents = driver.find_elements(By.CLASS_NAME, 'ArticleContentBox')
                prev_day = today
            except Exception as e:
                print(e)
                continue

            if len(contents) == 0:
                time.sleep(5)
                continue

            else:
                contents = contents[0].text
                kakao_log = band_info_parsing(contents, kakao_log)
                kakao_send(kakao_log)
                break


