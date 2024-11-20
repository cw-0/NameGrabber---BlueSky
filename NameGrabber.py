from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from pyfiglet import Figlet
from getpass import getpass
import winsound
import sys
import os

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RESET = "\033[0m"

handle_list = []
works = []

format = Figlet(font='Big')
creator = f"{PURPLE}Twitch{RESET} - CainKillEmAll - {RED}You{RESET}Tube"

def main():
    # Print Name Grabber by Cain kill em all
    header()
    time.sleep(3)
    input("\n\nPress any key to continue...")
    clear_console()

    # Users Credentials
    email = input("What's your email: ").strip()
    password = getpass("What's your password: ").strip()

    # Get list of handles to try
    create_handle_list()

    # Loop through handles returning ones that work
    make_account(email, password)

    # Closing Screen
    print("\n\n\n")
    print(format.renderText("SUCCESS!"))
    time.sleep(3)
    input("\n\n\nPress any key to Close...")


def header():
    print(format.renderText("Name Grabber"))
    print(creator.center(70)) 

def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def create_handle_list():
    try:
        with open("handles.txt", "r") as file:
            for name in file:
                handle_list.append(name.strip())
    except FileNotFoundError:
        print("File not found")

def add_handle_to_working(works):
    with open("Working.txt", "a") as file:
        for name in works:
            file.write(name + "\n")


def make_account(email, password):
    driver = webdriver.Chrome()
    driver.get("https://bsky.app/")
    wait = WebDriverWait(driver, 10)

    # click sign up
    button_sign_up = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Sign up']")))
    button_sign_up.click()

    # type email
    entry_email = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Enter your email address']")))
    entry_email.send_keys(email)

    #type password
    entry_password = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Choose your password']")))
    entry_password.send_keys(password)

    # click next
    time.sleep(2)
    button_next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Continue to next step']")))
    button_next.click()

    # Enter Handle
    for handle in handle_list:
        entry_handle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Input your user handle']")))
        entry_handle.clear()
        entry_handle.send_keys(handle)

        # click next
        button_next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Continue to next step']")))
        button_next.click()

        # Check if taken
        if handle_taken(driver):
            print(f"{CYAN}{handle}{RESET} is taken {RED}=({RESET} ")
            continue

        winsound.MessageBeep() # play sound
        print(f"{CYAN}{handle}{RESET} not taken. Testing Validity...")
        time.sleep(10)

        if check_reservation(driver):
            print(f"{CYAN}{handle}{RESET} is reserved for someone more important i guess... {YELLOW}=|{RESET} \n\n")
            captcha_back_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Go back to previous step']")))
            captcha_back_button.click()
            continue

        if check_invalid_code(driver):
            works.append(handle)
            add_handle_to_working(works)
            print(f"{CYAN}{handle}{RESET} is Available! {GREEN}=){RESET} ")
            print(f"Added to Working.txt \n\n")
            continue
        else:
            print(f"{CYAN}{handle}{RESET} not allowed lol you thought")
            
        if handle == handle_list[-1]:
            print("\n\nEnd of list")
            time.sleep(2)
            break
    
    print("\n\nEnd of list")
    time.sleep(2)
    driver.quit()


def handle_taken(driver):
    try:
        error_message = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'That handle is already taken.')]")))
        return True
    except:
        return False

def check_reservation(driver):
    try:
        error_message = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Reserved handle')]")))
        return True
    except:
        return False

def check_invalid_code(driver):
    try:
        error_message = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid verification code.')]")))
        return True
    except:
        return False


if __name__ == "__main__":
    main()
