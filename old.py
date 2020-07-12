import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from random import randint
from faker import Faker

faker = Faker()

ALL_PARTIES_COUNT = 3913043
mn, mx = 1000, 9999
fio = faker.name().lower().split(' ')
fio.append(str(randint(mn, mx)))
nickname = ''.join(fio)
mail = f'{nickname}@yahoo.com'
passwrd = f'admin@17{nickname}'

# print(f'data: {nickname}, {mail}/{passwrd}')


option = Options()
# option.add_argument("--headless")
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

prefs = {'safebrowsing.enabled': True,
         "select_file_dialogs.allowed": False,
         "download_restrictions": 0,
         "download.prompt_for_download": False,
         "download.directory_upgrade": True,
         "download.default_directory": '/Users/asvezh/PycharmProjects/chess/parties_1_100',
         "credentials_enable_service": False,
         "profile.password_manager_enabled": False,
         "profile.default_content_settings.popups": 0,
         "profile.default_content_setting_values.automatic_downloads": 1
         }
option.add_experimental_option('prefs', prefs)

browser = webdriver.Chrome(executable_path='./chromedriver',
                           chrome_options=option)
browser.implicitly_wait(5)
wait = WebDriverWait(browser, 10)

url_reg = 'http://chess.com/register'
url_login = 'http://chess.com/login_and_go'

# browser.get(url_reg)
# time.sleep(1)
#
# browser.find_element_by_id('registration_username').send_keys(nickname)
# browser.find_element_by_id('registration_email').send_keys(mail)
# browser.find_element_by_id('registration_password').send_keys(passwrd)
# browser.find_element_by_id('registration_submit').click()

browser.get(url_login)
nickname, mail, passwrd = 'jennasmith335', 'jennasmith335@yahoo.com', 'admin@17jennasmith335'
# nickname, mail, passwrd = 'elizabethliu3683', 'elizabethliu3683@yahoo.com', 'admin@17elizabethliu3683'
browser.find_element_by_id('username').send_keys(nickname)
browser.find_element_by_id('password').send_keys(passwrd)
browser.find_element_by_id('login').click()

# try:
#     browser.find_element_by_css_selector('span.icon-font-chess.x').click()
# except Exception as e:
#     print('without banners')

for line in range(1, 10):
    browser.get(f'http://chess.com/4-player-chess?g={line}')
    # wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.board-container')))
    time.sleep(5)
    # print('loadedGameChat:', browser.find_element_by_id('loadedGameChat').text)
    # browser.find_element_by_css_selector('.notifications-request-actions button').click()
    lst = browser.find_elements_by_css_selector('.tab .tab-title')
    _ = [line.click() for line in lst if 'PGN4' in line.text]

    buttons = browser.find_elements_by_css_selector('.pgn-buttons a')
    _ = [clck.click() for clck in buttons if 'Save' in clck.text]
    WebDriverWait(browser, 3).until(ec.alert_is_present(), 'File name?')
    browser.switch_to.alert.accept()

browser.quit()
