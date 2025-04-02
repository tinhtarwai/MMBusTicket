from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--incognito")  # Open in incognito mode
        options.add_argument("--disable-application-cache")  # Force disable cache (alternative)

        service = Service(r"C:/Users/A_R_T/AppData/Local/Drivers/chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        driver.maximize_window()
        return driver
    except Exception as e:
        raise RuntimeError(f"Failed to initialize WebDriver: {e}")

def open_url(driver, url):
    try:
        driver.get(url)
    except Exception as e:
        raise RuntimeError(f"Failed to open URL '{url}': {e}")
