import sys
import time

import pyperclip
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def create_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=512,512")

    # Use ChromeDriverManager to automatically download and manage the ChromeDriver executable
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    return browser


def wait(seed):
    seed.implicitly_wait(30)


def generate_password(n):
    import random
    import string
    password = ''
    for i in range(n):
        password += random.choice(string.ascii_letters + string.digits + string.punctuation + string.digits)
    return password


def write_credentials(username, password):
    with open('credentials.txt', 'w') as f:
        f.write(f"Username: {username}\nPassword: {password}")
        print("Credentials written to file")


def handle_error_block(driver):
    try:
        # Try to locate the error block element
        error_block = driver.find_element(By.XPATH, "/html/body/div[3]/div/div")

        # If NoSuchElementException is not raised, the error block is present
        print(error_block.text)
        sys.exit()

    except NoSuchElementException:
        # If NoSuchElementException is raised, the error block is not present
        print("Account created successfully, you have 50 seconds to verify your email address")
        time.sleep(50)
        sys.exit()


tmailor = create_browser()
tmailor.get("https://tmailor.com/en")
wait(tmailor)
time.sleep(2)
print("Copied email button clicked")
copy_email = tmailor.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[1]/div[1]/div[3]/button[1]')
copy_email.click()
wait(tmailor)

email = pyperclip.paste()
time.sleep(2)

seed = create_browser()
seed.get("https://seed4.me/")
wait(seed)
print("Navigated to seed4.me")

threeBars = seed.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/a[1]")
threeBars.click()
my_account = seed.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div/ul/li[8]/a")
my_account.click()
wait(seed)
print("Clicked on My Account")

create_seed4me_account = seed.find_element(By.XPATH, "/html/body/div[3]/div/div/a[2]")
create_seed4me_account.click()
wait(seed)
print("Clicked on Create Seed4.me Account")

email_textbox = seed.find_element(By.XPATH, "//*[@id=\"UserUsername\"]")
email_textbox.send_keys(email)
password_textbox = seed.find_element(By.XPATH, "//*[@id=\"UserPassword\"]")
password = generate_password(10)
password_textbox.send_keys(password)
confirm_password_textbox = seed.find_element(By.XPATH, "//*[@id=\"UserConfirmPassword\"]")
confirm_password_textbox.send_keys(password)
confirm = seed.find_element(By.XPATH, "//*[@id=\"UserAccept\"]")
confirm.click()
print("Filled in registration details")

register = seed.find_element(By.XPATH, "//*[@id=\"UserRegisterForm\"]/div[8]/div/input")
register.click()
print("Clicked on Register")

write_credentials(email, password)
print("Credentials written to file")
seed.close()
time.sleep(45)
#handle_error_block(seed)
sys.exit()

while True:
    pass
