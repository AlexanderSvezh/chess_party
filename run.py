from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from random import randint, choice
from collections import namedtuple
from datetime import datetime
from selenium import webdriver
from faker import Faker
import argparse
import time
import os


faker = Faker()
ALL_PARTIES_COUNT = 3913043


def browser(dir_name):
    option = Options()
    option.add_argument('--no-proxy-server')
    option.add_argument('--no-sandbox')
    option.add_argument("window-size=1920,1080")
    option.add_argument('--start-maximized')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-infobars')
    option.add_argument("--disable-extensions")
    option.add_argument('--disable-web-security')
    option.add_argument('--disable-software-rasterizer')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--safebrowsing-disable-extension-blacklist')
    option.add_argument('--safebrowsing-disable-download-protection')

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    prefs = {'safebrowsing.enabled': True,
             "select_file_dialogs.allowed": False,
             "download_restrictions": 0,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "download.default_directory": f'/Users/asvezh/PycharmProjects/chess/{dir_name}',
             "credentials_enable_service": False,
             "profile.password_manager_enabled": False,
             "profile.default_content_settings.popups": 0,
             "profile.default_content_setting_values.automatic_downloads": 1
             }
    option.add_experimental_option('prefs', prefs)
    instance = webdriver.Chrome(executable_path='./chromedriver',
                                chrome_options=option)
    instance.implicitly_wait(5)
    return instance


def registration(browser):
    mn, mx = 1000, 9999
    fio = faker.name().lower().split(' ')
    fio.append(str(randint(mn, mx)))
    nickname = ''.join(fio)
    mail = f'{nickname}@yahoo.com'
    passwrd = f'admin@17{nickname}'
    print(f'DATA: {nickname}, {mail}/{passwrd}')
    url_reg = 'http://chess.com/register'
    browser.get(url_reg)
    time.sleep(1)
    browser.find_element_by_id('registration_username').send_keys(nickname)
    browser.find_element_by_id('registration_email').send_keys(mail)
    browser.find_element_by_id('registration_password').send_keys(passwrd)
    time.sleep(10)
    browser.find_element_by_id('registration_submit').click()
    with open('users_data.txt', 'a+') as data:
        data.write(f"\n'{nickname}', '{mail}', '{passwrd}'")
    return browser


def login(browser, creds):
    nickname, passwrd = creds
    url_login = 'http://chess.com/login_and_go'
    browser.get(url_login)
    browser.find_element_by_id('username').send_keys(nickname)
    browser.find_element_by_id('password').send_keys(passwrd)
    browser.find_element_by_id('login').click()
    return browser


def click_banners(browser):
    try:
        browser.find_element_by_css_selector('span.icon-font-chess.x').click()
    except Exception as e:
        print('without banners', e)


def click_hint(browser):
    try:
        browser.find_element_by_css_selector('.notifications-request-actions button').click()
    except Exception as e:
        print('without banners2', e)


def crashlog(load_range, start, line):
    namerange = f'{load_range[0]}_{load_range[-1]}'
    prc = round((int(line)-load_range[0])/(load_range[-1]-load_range[0]) * 100, 1)
    log_str = f'{namerange}: {line} - {(datetime.now() - start).seconds} sec, {prc}%'
    print(log_str)
    with open(f'./logs/{namerange}.log', 'w') as logfile:
        logfile.write(log_str)


def download_games(browser, dirname, load_range):
    count = 0
    check = True
    wait = WebDriverWait(browser, 5)
    start_all = datetime.now()
    for line in load_range:
        start = datetime.now()
        browser.get(f'http://chess.com/4-player-chess?g={line}')
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.board-container')))
        if check:
            click_banners(browser)
            check = False
        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.tab .tab-title')))
        lst = browser.find_elements_by_css_selector('.tab .tab-title')
        _ = [line.click() for line in lst if 'PGN4' in line.text]
        browser.find_elements_by_css_selector('.pgn-buttons a')[-1].click()
        wait.until(ec.alert_is_present(), 'File name?')
        browser.switch_to.alert.accept()
        crashlog(load_range, start, line)
        count = check_directory_size(dirname, count)
    print(f'FINISH: {(datetime.now() - start_all).seconds} sec')


def check_directory_size(dr, count):
    limit = 10000
    num_files = len([f for f in os.listdir(dr)])
    if num_files > limit:
        count += 1
        newname = f'{dr}_{count}'
        os.rename(dr, newname)
    return count


def get_user():
    User = namedtuple('User', ['nickname', 'mail', 'passwrd'])
    userlist = [
        User('jennasmith335', 'jennasmith335@yahoo.com', 'admin@17jennasmith335'),
        User('elizabethliu3683', 'elizabethliu3683@yahoo.com', 'admin@17elizabethliu3683'),
        User('andrematthews6052', 'andrematthews6052@yahoo.com', 'admin@17andrematthews6052'),
        User('barbaraford9064', 'barbaraford9064@yahoo.com', 'admin@17barbaraford9064'),
        User('tylermartinez3561', 'tylermartinez3561@yahoo.com', 'admin@17tylermartinez3561'),
        User('mathewmoon2467', 'mathewmoon2467@yahoo.com', 'admin@17mathewmoon2467'),
        User('karenmccullough6178', 'karenmccullough6178@yahoo.com', 'admin@17karenmccullough6178'),
        User('richardcolon5651', 'richardcolon5651@yahoo.com', 'admin@17richardcolon5651')
    ]
    return choice(userlist)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='chess parser')
    parser.add_argument("--start")
    parser.add_argument("--finish")
    args = parser.parse_args()
    after, before = args.start, args.finish
    dirname = f'parties_{after}_{before}'
    chrome_instance = browser(dirname)
    nickname, mail, passwrd = get_user()
    try:
        session = login(chrome_instance, (nickname, passwrd))
        # session = registration(chrome_instance)
        download_games(session, dirname, range(int(after), int(before)+1))
    except Exception as err:
        print(repr(err))
        chrome_instance.save_screenshot('./logs/bugs.png')
    finally:
        chrome_instance.quit()
