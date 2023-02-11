import pickle
import random
import time

import pyautogui
import pyperclip
from selenium.webdriver.common.by import By

import config as cfg


def driver_sleep(driver, t_min:float=2, t_max:float=3):
    driver.implicitly_wait(15)
    time.sleep(random.randint(t_min, t_max))


def get_latest_article_num(driver, url):
    driver.get(url)  # today information article
    driver_sleep(driver, 2, 3)
    driver.switch_to.frame("cafe_main")

    # find today's article
    today, today_article_num = time.strftime('%Y-%m-%d', time.localtime(time.time())), -1
    tot_articles = driver.find_elements(By.CLASS_NAME, "td_article")
    for current_article in tot_articles:
        if today in current_article.text:
            today_article_num = current_article.text.split('\n')[0]
            break

    return today_article_num


def message_scheduler():
    current_hour = int(time.strftime('%H', time.localtime(time.time())))
    current_min = int(time.strftime('%M', time.localtime(time.time())))
    if current_hour >= 0 and current_hour < 10:
        with open(file=cfg.kakao_log, mode='wb') as f:
            pickle.dump({}, f)
        return False

    return True


def band_info_parsing(text, kakao_log):
    content_lines = text.split('\n')
    auction_idx = 1
    for line in content_lines:
        if '조회수' in line: state = ''

        if '[경매종료]' in line:
            state = '[종료] '
        elif '1. 경매 품종' in line:
            auction_subj = ''.join(line.split('1. 경매 품종:')[1:])
            auction_idx += 1

        elif '2. 경매 시간' in line:
            end_time = ''.join(line.split('2. 경매 시간 (종료시간):')[1:]).split('.')[0]

        elif '3. 현재 최고가' in line:
            current_price = ''.join(line.split('3. 현재 최고가:')[1:]).split('.')[0] + '만원 '

        elif '5. 경매 링크' in line:
            url = ''.join(line.split('5. 경매 링크:')[1:])
            if url in kakao_log:
                _, _, _, _, _, send_state, dead = kakao_log[url]
                if '종료' in state: send_state = False
                kakao_log[url] = ('[낙찰]', auction_subj, current_price, url, end_time, send_state, dead)
            else:
                kakao_log[url] = ('[경매]', auction_subj, current_price, url, end_time, False, False)

    return kakao_log


def kakao_send(kakao_log):
    for auction_idx, auction in enumerate(kakao_log):
        state, auction_subj, current_price, url, end_time, send_state, dead = kakao_log[auction]
        if send_state or dead: continue

        if '[경매]' in state or '[낙찰]' in state:
            if '[경매]' in state:
                current_article= (state + auction_subj + end_time + url)
            else:
                current_article = (state + auction_subj + current_price + url)
            pyperclip.copy(current_article)
            time.sleep(random.randint(2, 4))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(random.randint(2, 4))
            pyautogui.press('enter')  # 제목을 입력해주세요
            time.sleep(1)

            if '[낙찰]' in state:
                kakao_log[auction] = state, auction_subj, current_price, url, end_time, True, True
            else:
                kakao_log[auction] = state, auction_subj, current_price, url, end_time, True, False

    with open(file=cfg.kakao_log, mode='wb') as f:
        pickle.dump(kakao_log, f)

    time.sleep(random.randint(50, 90))