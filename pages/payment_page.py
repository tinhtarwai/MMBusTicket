import random
import time

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
    mock_pay = (By.XPATH, "//div[normalize-space()='Mock Pay']")
    pin_box = (By.XPATH, "//input[@name='meaningOfLife']")
    pay_btn = (By.XPATH, "//button[normalize-space()='Pay Now']")
    proceed_to_pay_btn = (By.XPATH, "//a[normalize-space()='Proceed To Pay']")
    merchant_btn = (By.XPATH, "//a[normalize-space()='Return to Merchant']")
    confirm_page_ele = (By.XPATH, "//span[@class='success-text']")


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
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def get_random_payment(self):
        by, value = self.payment_list
        payment_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((by, value))
        )
        selected_payment = random.choice(payment_list)
        selected_payment.click()

    def choose_mock_pay(self):
        by, value = self.mock_pay
        try:
            mock = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
            )
            if mock.is_displayed():
                mock.click()
            else:
                print("\nElement is not displayed.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def mock_payment(self, pin):
        try:
            pin_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.pin_box)
            )
            pin_box.send_keys(pin)
            time.sleep(2)
            pay_now = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.pay_btn)
            )
            if pay_now.is_displayed():
                pay_now.click()
            else:
                print("Pay Now button not found")
        except Exception as e:
            print(f"An error occurred: {e}")

    def redirect_to_complete(self):
        try:
            return_to_mer = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.merchant_btn)
            )
            if return_to_mer.is_displayed():
                return_to_mer.click()
            else:
                print("Pay Now button not found")
        except Exception as e:
            print(f"An error occurred while redirecting to merchant page")

        # redirect to booking complete page
        try:
            confirm_ele = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.confirm_page_ele)
            )
            print("Your Booking process is successful and confirmed.")
            return confirm_ele
        except Exception as e:
            print(f"An error occurred while redirecting to booking complete page.")


    def get_validation_message(self):
        by, value = self.validation_msg
        msg = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by,value))
        )
        return msg.text