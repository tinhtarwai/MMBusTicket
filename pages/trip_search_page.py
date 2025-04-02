from datetime import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TripSearchPage:
    def __init__(self, driver):
        self.driver = driver

    source_dropdown = (By.XPATH, "//select[@id='selectFrom']")
    destination_dropdown = (By.XPATH, "//select[@id='selectTo']")
    source = (By.XPATH, "//span[@title='From']")
    destination = (By.XPATH, "//span[@title='To']")

    source_dropdown_text = (By.XPATH, "//span[@title='From']//span[@class='text-dark']")
    destination_dropdown_text = (By.XPATH, "//span[@title='To']//span[@class='text-dark']")
    search_field = (By.XPATH, "//input[@role='searchbox']")

    depart_date = (By.XPATH, "//div[@class='area-departure-date']")
    date_display = (By.XPATH, "//span[@id='date-display']")
    month_year = (By.XPATH, "//div[@id='month-year-label']")
    days = (By.XPATH, "//div[@data-day-cell]")
    date_forward_arrow = (By.XPATH, "//div[@id='header']//div[3]")
    nationality = (By.XPATH, "//div[@class='area-nationality d-flex']//input")
    search_btn = (By.XPATH, "//div[@class='area-search-button']")

    plus_seat_btn = (By.XPATH, "//button[@id='increment-counter']")
    minus_seat_btn = (By.XPATH, "//button[@id='decrement-counter']")
    seat_display = (By.XPATH,"//span[@id='countDisplay' and not(contains(@class, 'text-muted'))]")

    empty_result_source = (By.XPATH, "//ul[@id='select2-selectFrom-results']")
    empty_result_destination = (By.XPATH, "//ul[@id='select2-selectTo-results']")

    focus_click = (By.XPATH, "//div[@class='banner-heading']")
    disabled_destination = (By.XPATH, "//span//ul[@id='select2-selectTo-results']//li[@aria-disabled='true']")
    muted_destination = (By.XPATH, "//span[@id='select2-selectTo-container']//span[@class='text-muted']")

    trip_count_display = (By.XPATH, "(//div[@class='trip-searched-description'])[2]")
    empty_res_text1 = (By.XPATH, "//div[@class='text-center p-5 m-5']//h3")
    empty_res_text2 = (By.XPATH, "//div[@class='text-center p-5 m-5']//i")

    def select_location(self, location, dropdown_locator):
        by, value = dropdown_locator
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(location)

    def enter_location(self, location, dropdown_locator, search_field):
        self.driver.find_element(*dropdown_locator).click()
        self.driver.find_element(*search_field).send_keys(location)

    def get_location_empty_result(self,empty_result_location):
        by, value = empty_result_location
        return self.driver.find_element(by, value).text

    def get_location_text(self, dropdown_locator):
        by, value = dropdown_locator
        return self.driver.find_element(by, value).text

    def get_element_disabled(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            is_disabled = element.get_attribute("disabled") is not None
            is_aira_disabled = element.get_attribute("aria-disabled") is not None
            return is_disabled or is_aira_disabled
        except:
            return False  # Element not found or not disabled

    def get_disabled_location_text(self, disabled_location):
        # disabled_loc = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_all_elements_located(disabled_location)
        # )
        # disabled_element = None
        # for dis in disabled_loc:
        #     if dis.get_attribute("disabled") in ["disabled", "true"]:
        #         disabled_element = dis
        #         break  # Stop looping after finding the first matching element
        #
        # if disabled_element:
        #     disabled_text = disabled_element.text.strip()
        #     return disabled_text if disabled_text else "No visible text found"
        # else:
        #     print("No disabled element found.")

        disabled_loc = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(disabled_location)
        )
        if disabled_loc:
            disabled_text = disabled_loc.text.strip()
            return disabled_text if disabled_text else "No visible text found"
        else:
            print("No disabled element found.")

    def is_destination_muted(self, muted_desti):
        muted_destination = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(muted_desti)
        )
        return muted_destination.text if muted_destination else print("Error")

    def clear_locations(self, source, destination):
        source_dd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(source)
        )
        destination_dd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(destination)
        )
        self.driver.execute_script("arguments[0].value = '';", source_dd)
        self.driver.execute_script("arguments[0].value = '';", destination_dd)

    def choose_departure_date(self, year, month, date):
        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
        month_number = datetime.strptime(month, "%B").month  # Converts to 2

        # check if the requested date is in the past
        today_date = datetime.today().date()
        requested_date = datetime(year, month_number, date).date()
        if requested_date < today_date:
            print(f"Error : Cannot select, {requested_date} is a past date!")
            return

        while True:
            month_year_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.month_year))
            mon_yr = month_year_element.text.strip()
            print("Current month-year label:", mon_yr)
            if mon_yr.lower().strip() == f"{month} {year}".lower().strip():
                break

            self.driver.find_element(*self.date_forward_arrow).click()
            wait.until(
                EC.text_to_be_present_in_element((By.ID, "month-year-label"), f"{month} {year}"))
        time.sleep(1)
        wait.until(EC.presence_of_all_elements_located(self.days))
        days = self.driver.find_elements(*self.days)

        for day in days:
            day_text = day.get_attribute("data-day-cell")  # Get full date (YYYY-MM-DD)

            if day_text == f"{year}-{month_number:02d}-{date:02d}":  # Ensure proper format
                # check if the day is disabled
                if "calendar-cell-disabled" in day.get_attribute("class"):
                    print(f"Error : {day_text} is disabled and cannot be selected. ")

                print(f"Clicking on: {day_text}")  # Debugging
                self.driver.execute_script("arguments[0].scrollIntoView();", day)
                time.sleep(0.5)  # Ensure the UI settles
                self.driver.execute_script("arguments[0].click();", day)
                break

        chosen_date = wait.until(EC.presence_of_element_located(self.date_display)).text
        print("Final chosen date:", chosen_date)

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

    def get_count(self, display):
        by, value = display
        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
        element = wait.until(EC.visibility_of_element_located((by, value)))
        text = element.text.strip()
        print(f"Extracted text: {text}")  # Debugging

        # Ensure the text contains a valid number
        if text and text.split()[0].isdigit():
            return int(text.split()[0])
        else:
            raise ValueError(f"Unexpected format: {text}")  # Handle unexpected format


    def choose_nationality(self, nationality_type):
        nationality_list = self.driver.find_elements(*self.nationality)
        for i in nationality_list:
            if i.get_attribute("id")==nationality_type:
                i.click()
                break

    def get_validation_message(self, element_locator):
        by, value = element_locator
        element = self.driver.find_element(by, value)
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    def get_form_validation_message(self):
        return self.driver.execute_script("""
            var form = document.querySelector('form');
            if (!form.checkValidity()) {
                // Find the first invalid field
                var invalidField = form.querySelector(':invalid');
                return invalidField ? invalidField.validationMessage : 'No validation message found';
            }
            return 'Form is valid';
        """)

    def get_empty_result_texts(self):
        wait = WebDriverWait(self.driver, 5)  # Wait up to 10 seconds
        text1 = wait.until(EC.visibility_of_element_located(self.empty_res_text1)).text
        text2 = wait.until(EC.visibility_of_element_located(self.empty_res_text2)).text
        print(text1, text2)
        return text1, text2