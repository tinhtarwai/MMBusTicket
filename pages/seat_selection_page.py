from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeatSelectionPage:
    def __init__(self, driver):
        self.driver = driver

    available_seats = (By.XPATH,"(//table//tbody//tr/td//a[@class='seat seat-available'])")
    all_seats = (By.XPATH, "(//table[@id='seat-table'])//td//a")
    proceed_btn = (By.XPATH, "//div[@class='card-body border-top']//button[@type='button']")

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
            proceed_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.proceed_btn)
            )
            proceed_button.click()
        except Exception as e:
            raise RuntimeError(f"Failed to click the Proceed button: {e}")
