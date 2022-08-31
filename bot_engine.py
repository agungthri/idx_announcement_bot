from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from telegram_bot import send_message

import random 
import time
import json

# initiate web driver with selenium
def set_driver():
    options = Options()
    ser = Service('chromedriver.exe')
    options.add_argument("start-maximized")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=ser, options=options)
    return driver

# set driver to get data
def get_data(driver):
    driver.get('https://www.idx.co.id/umbraco/Surface/NewsAnnouncement/GetAllAnnouncement?pageNumber=1&pageSize=10&language=id-id')
    data = driver.find_element(By.TAG_NAME, "pre")
    all_data = []
    for i in json.loads(data.text)['Items']:
        PublishDate = i['PublishDate']
        Title = i['Title']
        Code = i['Code']
        link_all = []
        for j in i['Attachments']:
            link = f"https://www.idx.co.id{j['FullSavePath']}"
            link_all.append(link)
        all_data.append([PublishDate, Title, Code, link_all])
        
    return all_data

# extract data to get readable message
def to_send(data : list):
    to_send = f"{data[0]} \n\n {data[1]} - {data[2]} \n\n"
    c = 0
    for i in data[3]:
        c += 1
        to_send = to_send + f"LINK - {c} \n {i} \n"
        
    send_message(to_send)

# add time to get bot slept
def add_time():
    time.sleep(random.randint(5, 15))

# looping process to get semi real-time data
def main():
    driver = set_driver()
    all_data = get_data(driver)

    while 1:

        add_time()

        try:

            for i in get_data(driver):
                if i in all_data:
                    pass
                else:
                    to_send(i)
                    all_data.append(i)

        except WebDriverException as e:
            send_message("WebDriverException")
            continue

        except NoSuchElementException as e:
            send_message("NoSuchElementException")
            continue
