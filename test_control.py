from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from devtools_ai.selenium import SmartDriver

def main():
    """Main driver"""
    chrome_driver = Chrome(service=Service(ChromeDriverManager().install()))

    # Convert chrome_driver to smartDriver
    driver = SmartDriver(chrome_driver, "baa7f39e7710ec314bc9b618")
    # Navigate to Google.com
    driver.get("https://myntra.com")
    sleep(1)

    # Find the searchbox and send "hello world"
    searchbox_element = driver.find_element(By.NAME, "q")
    searchbox_element.send_keys("hello world\n")

    sleep(2)

    driver.quit()


if __name__ == "__main__":
    main()