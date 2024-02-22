# -*- coding: utf-8 -*-
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import signal

# Global variables
room_code=""
num_browsers=5
option=0
pool=None

# Signal handler
def signal_handler(signal, frame):
    print("\n\nSaliendo...")
    pool.terminate()
    pool.join()
    exit(0)

# Functions
def spam_emoji(_):
    emoji='span.sc-gVcvut.dNEQJg'
    
    driver = webdriver.Firefox()
    driver.get(f'https://app.wooclap.com/{room_code}?from=banner')
    
    # First button
    button = driver.find_element(By.CSS_SELECTOR, 'span.sc-gVcvut.dNEQJg')
    button.click()
    # Wait for the button to be clickable
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, emoji)))

    # Click the button
    while True:
        button.click()

def spam_user(_):
    while True:
        driver = webdriver.Firefox()
        driver.get(f'https://app.wooclap.com/{room_code}?from=banner')
        driver.quit()
        
def menu():
    global room_code, num_browsers, option
    print("===Wooclap Spammer===")
    print("\n")
    room_code = input("Introduce el codigo de la sala (Ej= LKPLYb): ")
    num_browsers = int(input("¿Cuantos navegadores quieres usar? (Ej= 5): "))
    print("Selecciona una opción: ")
    print("\t1. Spam Emoji")
    print("\t2. Spam User")
    option = int(input("Opción: "))

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
    
