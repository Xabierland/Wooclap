# -*- coding: utf-8 -*-
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import signal
import random
import string

# Global variables
room_code=""
num_browsers=5
option=0
login=False
emoji='👍'
pool=None

# Signal handler
def signal_handler(signal, frame):
    print("\n\nSaliendo...")
    pool.terminate()
    pool.join()
    exit(0)

def generate_random_user(driver):
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    # Find the input field and enter the username
    input_field = driver.find_element(By.CSS_SELECTOR, 'input.sc-hWkvll.jbinJd')
    input_field.send_keys(username)
    # Find the button and click it
    button = driver.find_element(By.CSS_SELECTOR, 'button.sc-TWmSL.lfMRjh')
    button.click()

def select_emoji():
    global emoji
    try:
        emoji_option = int(input("Selecciona el emoji a usar:\n\t1. 👍\n\t2. 💙\n\t3. 🔥\n\t4. 😯\n\t5. 🎉\n\t6. Aleatorio\nOpción: "))
    except EOFError:
        print("No se ha proporcionado ninguna entrada.")
        emoji_option = 1

    # Determine the emoji based on the selected option
    if emoji_option == 1:
        emoji = '👍'
    elif emoji_option == 2:
        emoji = '💙'
    elif emoji_option == 3:
        emoji = '🔥'
    elif emoji_option == 4:
        emoji = '😯'
    elif emoji_option == 5:
        emoji = '🎉'
    elif emoji_option == 6:
        emoji = 'Random'
    else:
        print("Opción inválida. Se usará el emoji por defecto.")
        emoji = '👍'

# Functions
def spam_emoji(_):
    driver = webdriver.Firefox()
    driver.get(f'https://app.wooclap.com/{room_code}?from=banner')

    if login:
        generate_random_user(driver)

    # First button
    button = driver.find_element(By.CSS_SELECTOR, 'span.sc-gVcvut.dNEQJg')
    button.click()

    # Find the next button to click based on the desired emoji
    if emoji == '👍':
        button = driver.find_element(By.CSS_SELECTOR, 'div.sc-igdSGC.knWWDE button:nth-child(1)')
    elif emoji == '💙':
        button = driver.find_element(By.CSS_SELECTOR, 'div.sc-igdSGC.knWWDE button:nth-child(2)')
    elif emoji == '🔥':
        button = driver.find_element(By.CSS_SELECTOR, 'div.sc-igdSGC.knWWDE button:nth-child(3)')
    elif emoji == '😯':
        button = driver.find_element(By.CSS_SELECTOR, 'div.sc-igdSGC.knWWDE button:nth-child(4)')
    elif emoji == '🎉':
        button = driver.find_element(By.CSS_SELECTOR, 'div.sc-igdSGC.knWWDE button:nth-child(5)')
    
    # Click the button
    while True:
        if emoji == 'Random':
            button = driver.find_element(By.CSS_SELECTOR, 'div.sc-igdSGC.knWWDE button:nth-child(' + str(random.randint(1, 5)) + ')')
        button.click()

        
def spam_user(_):
    while True:
        if login:
            generate_random_user(driver)
        driver = webdriver.Firefox()
        driver.get(f'https://app.wooclap.com/{room_code}?from=banner')
        driver.quit()
        
def menu():
    global room_code, num_browsers, option, login
    print("===Wooclap Spammer | by Xabierland===")
    room_code = input("Introduce el codigo de la sala (Ej= LKPLYb): ")
    num_browsers = int(input("¿Cuantos navegadores quieres usar? (Ej= 5): "))
    login = bool(input("¿Quieres iniciar sesión? (S/N): "))
    print("Selecciona una opción: ")
    print("\t1. Spam Emoji")
    print("\t2. Spam User")
    option = int(input("Opción: "))
    if option == 1:
        select_emoji()

def switch_function(i):
    global pool
    switcher = {
        1: lambda: pool.map(spam_emoji, range(num_browsers)),
        2: lambda: pool.map(spam_user, range(num_browsers))
    }
    func = switcher.get(i, lambda: None)
    func()

# Main
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    menu()
    pool = Pool(num_browsers)
    switch_function(option)
    
