import sys
import time
import random
import string
import pyperclip
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Constants
URL_TMAILOR = "https://tmailor.com/en"
URL_SEED = "https://seed4.me/"
WAIT_TIME = 30
PASSWORD_LENGTH = 10


def create_browser():
    browserOptions = Options()
    browserOptions.add_argument("--window-size=512,512")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browserOptions)
    return browser


def wait(browser):
    browser.implicitly_wait(WAIT_TIME)


def generate_password(n):
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(n))
    return password


def write_credentials(username, password):
    with open('credentials.txt', 'w') as f:
        f.write(f"Username: {username}\nPassword: {password}")
        print("Credentials written to file")


def handle_error_block(driver):
    try:
        error_block = driver.find_element(By.CSS_SELECTOR, ".alert.alert-block.alert-error.fade.in.out")
        print(error_block.text)
        sys.exit()
    except NoSuchElementException:
        print("Account created successfully, you have 50 seconds to verify your email address")
        time.sleep(50)
        sys.exit()


def main():
    tmailor = create_browser()
    tmailor.get(URL_TMAILOR)
    wait(tmailor)
    time.sleep(2)
    copy_email = tmailor.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[1]/div[1]/div[3]/button[1]')
    copy_email.click()
    print("Email copied to clipboard")
    wait(tmailor)
    email = pyperclip.paste()
    time.sleep(2)
    seed = create_browser()
    seed.get(URL_SEED)
    wait(seed)
    threebars = seed.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/a[1]")
    threebars.click()
    my_account = seed.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div/ul/li[8]/a")
    my_account.click()
    wait(seed)
    create_seed4me_account = seed.find_element(By.XPATH, "/html/body/div[3]/div/div/a[2]")
    create_seed4me_account.click()
    wait(seed)
    email_textbox = seed.find_element(By.XPATH, "//*[@id=\"UserUsername\"]")
    email_textbox.send_keys(email)
    password_textbox = seed.find_element(By.XPATH, "//*[@id=\"UserPassword\"]")
    password = generate_password(PASSWORD_LENGTH)
    password_textbox.send_keys(password)
    confirm_password_textbox = seed.find_element(By.XPATH, "//*[@id=\"UserConfirmPassword\"]")
    confirm_password_textbox.send_keys(password)
    confirm = seed.find_element(By.XPATH, "//*[@id=\"UserAccept\"]")
    confirm.click()
    register = seed.find_element(By.XPATH, "//*[@id=\"UserRegisterForm\"]/div[8]/div/input")
    register.click()
    write_credentials(email, password)
    handle_error_block(seed)
    seed.close()
    sys.exit()


if __name__ == "__main__":
    main()
