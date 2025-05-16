import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from pynput import keyboard
import time

options = uc.ChromeOptions()

driver = uc.Chrome(options=options, headless=False)

driver.get("https://login.fyers.in/")

print("Browser will remain open until ESC key is pressed...")

def on_press(key):
    if key == keyboard.Key.esc:
        print("ESC key pressed. Closing browser...")
        driver.quit()
        return False

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Script ended")