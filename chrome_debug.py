from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
import subprocess

# subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp')

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome('chromedriver', options=chrome_options)

# driver.switch_to.frame("cafe_main")

# fail_bttn = driver.find_elements(By.CLASS_NAME, "se-fallover-information")
# if len(fail_bttn) > 0:
#     print("Network failure...")

time.sleep(5)

pyautogui.press('enter')
# driver_sleep(driver, 1, 2)
# tabs = driver.window_handles
# driver.switch_to.window(tabs[-1])
time.sleep(2)
driver.close()
pyautogui.press('enter')
time.sleep(2)
driver.switch_to.window(driver.window_handles[-1])


