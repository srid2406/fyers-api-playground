import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard
from time import sleep

options = uc.ChromeOptions()
driver = uc.Chrome(options=options, headless=False)

driver.get("https://login.fyers.in/")
print("Waiting 40 seconds for manual login...")
sleep(40)

if driver.current_url.startswith("https://trade.fyers.in"):
    print("Login successful. Opening new tab...")
    driver.switch_to.new_window("tab")
    driver.get("https://trade.fyers.in")
    sleep(10)

    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        print("Switched to iframe.")

        chart_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.chart-markup-table.pane"))
        )

        actions = ActionChains(driver)
        actions.move_to_element(chart_div).click().perform()
        sleep(1)

        print("Chart focused. Sending Alt+G...")
        actions = ActionChains(driver)
        actions.key_down(Keys.ALT).send_keys('g').key_up(Keys.ALT).perform()
        sleep(2)
        dialog_wrapper = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "wrapper-b8SxMnzX")
            )
        )
        print("Date picker dialog wrapper detected.")

        date_input = WebDriverWait(dialog_wrapper, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input.input-RUSovanF')
            )
        )
        print("Date input field found.")
        
        value = date_input.get_attribute("value")
        print(f"Input value set to: {value}")

        driver.execute_script("""
            const input = arguments[0];
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, arguments[1]);
            input.dispatchEvent(new Event('input', { bubbles: true }));
        """, date_input, "2024-05-19")

        
        go_to_button = WebDriverWait(dialog_wrapper, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button-D4RPB3ZC"))
        )
        go_to_button.click()
        print("Go to button clicked.")

        print("Date set successfully.")

    except Exception as e:
        print("Error during chart interaction:")
        print(e)

else:
    print(f"Still on {driver.current_url}. Login might not have completed.")

print("Browser will remain open until ESC key is pressed...")

def on_press(key):
    if key == keyboard.Key.esc:
        print("ESC key pressed. Closing browser...")
        driver.quit()
        return False

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Script ended.")
