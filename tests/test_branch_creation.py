from selenium.webdriver.common.by import By

traveler_name = (By.XPATH, "//input[@id='name']")
phone_number = (By.XPATH, "//input[@id='phoneNumber']")
gender = (By.XPATH, "//input[@name='gender']")
email = (By.XPATH, "//input[@id='email']")
continue_btn = (By.XPATH, "//button[@id='traveller-info-submit-button']")
next_page_ele = (By.XPATH, "//ol[@class='steps']")