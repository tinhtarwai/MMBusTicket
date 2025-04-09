from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeatSelectionPage:
    def __init__(self, driver):
        self.driver = driver

    available_seats = (By.XPATH,"(//table//tbody//tr/td//a[@class='seat seat-available'])")
    all_seats = (By.XPATH, "(//table[@id='seat-table'])//td//a")
    proceed_btn = (By.XPATH, "//div[@class='card-body border-top']//button[@type='button']")
    proceed_btn1 = (By.XPATH, "//button[contains(., 'Continue to Traveller Info')]")

    def get_available_seats(self):
        return self.driver.find_elements(*self.available_seats)

    def get_all_seats(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.all_seats)
        )

    def click_seat(self, seat):
        seat.click()

    def get_seat_class(self, seat):
        return seat.get_attribute("class")

    def click_proceed_button(self):
        try:
            # proceed_button = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located(self.proceed_btn1)
            # )
            #
            # self.driver.execute_script("arguments[0].scrollIntoView(true);", proceed_button)
            #
            # proceed_button.click()

            buttons = self.driver.find_elements(*self.proceed_btn1)
            visible_buttons = [btn for btn in buttons if btn.is_displayed()]

            if not visible_buttons:
                raise Exception("No visible 'Continue to Traveller Info' button found.")
            elif len(visible_buttons) > 1:
                print("⚠️ Multiple visible buttons found. Clicking the first one.")

            visible_buttons[0].click()

        except Exception as e:
            print("Full error:", str(e))
            raise RuntimeError(f"Failed to click the Proceed button: {e}")
