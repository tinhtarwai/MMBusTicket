import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TravelerInfoPage:
    def __init__(self, driver):
        self.driver = driver

    traveler_name = (By.XPATH, "//input[@id='name']")
    phone_number = (By.XPATH, "//input[@id='phoneNumber']")
    gender = (By.XPATH, "//input[@name='gender']")
    email = (By.XPATH, "//input[@id='email']")
    continue_btn = (By.XPATH, "//button[@id='traveller-info-submit-button']")
    next_page_ele = (By.XPATH, "//ol[@class='steps']")

    input_fields = {
        "name": traveler_name,
        "phone": phone_number,
        "email": email
    }

    def get_input_field_locator(self, field_name):
        return self.input_fields.get(field_name)

    def fill_info(self, locator, value):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        field.clear()
        field.send_keys(value)

    def click_element(self, click_element):
        by, value = click_element
        ele = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        try:
            ele.click()
        except:
            # self.driver.execute_script("arguments[0].scrollIntoView();", ele)
            self.driver.execute_script("arguments[0].click();", ele)

    def get_validation_message(self, element_locator):
        by, value = element_locator
        element = self.driver.find_element(by, value)
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    def enter_data(self, field, data):
        by, value = field
        element = self.driver.find_element(by, value)
        element.clear()
        element.send_keys(data)

    def get_random_gender(self, gender_field):
        by, value = gender_field
        genders = self.driver.find_elements(by, value)
        if genders:
            random.choice(genders).click()
        else:
            print("no radio button found!")

    def get_element(self, ele):
        by, value = ele
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        if element:
            return True
        else:
            return False

