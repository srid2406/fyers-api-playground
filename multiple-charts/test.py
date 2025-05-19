import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def main():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, headless=False)

    try:
        driver.get("https://login.fyers.in/")
        print("Waiting 40 seconds for manual login...")
        sleep(40)

        if driver.current_url.startswith("https://trade.fyers.in"):
            print("Login successful. Opening new tab...")
            driver.switch_to.new_window("tab")
            driver.get("https://trade.fyers.in")
            sleep(5)

            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            print("Switched to iframe.")

            wait = WebDriverWait(driver, 10)
            try:
                pane_div = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.chart-markup-table.pane"))
                )
                print("Pane detected inside iframe!")
            except Exception as e:
                print("Pane NOT detected inside iframe.")
                print(e)

        else:
            print("Login not detected. Current URL:", driver.current_url)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
