import random

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PaymentPage:
    def __init__(self, driver):
        self.driver = driver

    payment_list = (By.XPATH, "//div[@class='mb-2 card card-clickable']")
    promo_field = (By.XPATH, "//div[@class='d-flex justify-content-end align-items-center text-success']")
    promo_box = (By.XPATH, "//input[@placeholder='Promo Code']")
    apply_btn = (By.XPATH, "//button[normalize-space()='Apply']")
    sub_total = (By.XPATH, "//div[contains(text(), 'Subtotal')]/following-sibling::div")
    convenient_fee = (By.XPATH, "//div[contains(text(), 'Convenience Fees')]/following-sibling::div")
    discount_amt = (By.XPATH, "//div[@class='d-flex align-items-center ']/following-sibling::div")
    total = (By.XPATH, "//div[contains(text(), 'Total')]/following-sibling::div")
    validation_msg = (By.XPATH, "//small[@class='ms-2 ml-2 mt-2 text-danger']")

    def enter_promo(self, promo_code, promo_field):
        by, value = promo_field
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        field.clear()
        field.send_keys(promo_code)

    def get_total_calculation(self):
        subtotal_ele = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((self.sub_total))
        )
        fee_ele = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((self.convenient_fee))
        )
        try:
            discount_ele = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.discount_amt))
            )
            discount_text = discount_ele.text.split(") ")[1]
            discount = discount_text.replace(",", "")
        except TimeoutException:
            discount = "0"
            print("⚠️ No discount element found")

        subtotal = subtotal_ele.text.replace(',','')
        fee = fee_ele.text

        print(subtotal , " ", fee, " ", discount)
        calculated_total = (int(subtotal)+ int(fee)) - int(discount)
        print("Calculated total amount : ", calculated_total)
        return calculated_total

    def get_total_amount(self, tot_amt):
        by, value = tot_amt
        total_amt_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        amount_text = total_amt_field.text
        total_amount = amount_text.split(' ')[1].replace(",", "")
        print("Display total amount : ", total_amount)
        return total_amount

    def click_element(self, ele):
        by, value = ele
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        try:
            element.click()
        except:
            self.driver.execute_script("argument[0].click();", element)

    def get_random_payment(self):
        by, value = self.payment_list
        payment_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((by, value))
        )
        selected_payment = random.choice(payment_list)
        selected_payment.click()


    # def get_validation_message(self, field):
    #     by, value = field
    #     element = self.driver.find_element(by, value)
    #
    #     WebDriverWait(self.driver, 10).until(
    #         lambda driver: driver.execute_script("return[0].validationMessage;", element) != ""
    #     )
    #     return self.driver.execute_script("return argument[0].validationMessage;", element)

    def get_validation_message(self):
        by, value = self.validation_msg
        msg = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by,value))
        )
        return msg.text