import random
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TripResultPage:
    def __init__(self, driver):
        self.driver = driver

    trip_count_display = (By.XPATH, "//div[@class='trip-searched-description'][2]")
    trip_result = (By.XPATH, "//div[@class='mb-3 trip-result']")
    filter_trip_result = (By.XPATH, "//div[@class='mb-3 trip-result' and @style!='display: none;']")
    empty_filter_result = (By.XPATH, "//div[@id='filtered-trip-results-empty']")
    plus_btn = (By.XPATH, "//button[@id='increment-counter']")
    search_btn = (By.XPATH, "//div[@class='area-search-button']")
    display_seat_price = (By.XPATH, "//div[@class='area-action']//span[contains(text(),'seat')]")
    request_seat = (By.XPATH, "//span[@id='countDisplay']")
    total_amt = (By.XPATH, "//div[@class='area-action']//div[@class='lead text-success']")
    display_time_of_day = (By.XPATH, "//div[@class='trip-result-content-title']//small//span")
    time_filter = (By.XPATH, "//input[@name='time_option']")
    operator_filter = (By.XPATH, "//input[@name='operator_option']")
    display_depart_time = (By.XPATH, "//div[@class='area-trip-info']//small[@class='waypoint-schedule text-body-sm'][1]")
    display_arrival_time = (By.XPATH, "//div[@class='area-trip-info']//small[@class='waypoint-schedule text-body-sm'][2]")
    display_duration = (By.XPATH, "//div[@class='small text-muted mt-2 d-flex align-items-center']")
    source_dropdown_text = (By.XPATH, "//span[@title='From']//span[@class='text-dark']")
    destination_dropdown_text = (By.XPATH, "//span[@title='To']//span[@class='text-dark']")
    display_source = (By.XPATH, "//div[@class='itinerary itinerary-sm mt-2']//small[@class='waypoint-name text-body-sm'][1]")
    display_destination = (By.XPATH, "//div[@class='itinerary itinerary-sm mt-2']//small[@class='waypoint-name text-body-sm'][2]")

    def get_trip_count(self, count_display):
        by, value = count_display
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((by, value)))
        text = element.text.strip()
        if text and text.split()[0].isdigit():
            return int(text.split()[0])
        else:
            raise ValueError(f"Unexpected format: {text}")

    def available_trips(self, trip_result):
        by, value = trip_result
        wait = WebDriverWait(self.driver, 10)
        result_list = wait.until(EC.presence_of_all_elements_located((by, value)))
        return len(result_list), result_list

    def random_seat_number(self, min_seat, max_seat):
        random_no = random.randint(min_seat,max_seat)
        print ("random no - ", random_no)
        return random_no

    def click_element(self, click_element):
        by, value = click_element
        ele = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        try:
            ele.click()
        except:
            self.driver.exexute_script("arguments[0].click();", ele)

    def get_display_seat_or_price(self, display_seat_price):
        by, value = display_seat_price
        seat_count = []
        price = []
        wait = WebDriverWait(self.driver, 10)
        display_seat_text = wait.until(EC.presence_of_all_elements_located((by, value)))
        for seat_price in display_seat_text:
            original_text = seat_price.text
            seat_count_text = re.search(r'(\d+\sseats?)\sx', original_text)
            if seat_count_text:
                seat_count.append(seat_count_text.group(1))

            price_text = re.search(r'x\s(.*)', original_text)
            if price_text:
                price.append(price_text.group(1))
        return seat_count, price

    def get_total_amount(self, total_amount):
        by, value = total_amount
        tot_amt = []
        amount_text = self.driver.find_elements(by, value)
        for amount in amount_text:
            original_text = amount.text
            total_price_text = re.search(r'\s(.*)', original_text)
            if total_price_text:
                tot_amt.append(total_price_text.group(1))

        return tot_amt


    def get_data(self, search_data):
        by, value = search_data
        display_data = self.driver.find_element(by, value).text
        return display_data


    def get_depart_arrival_time(self, time):
        by, value = time
        time_text = []
        display_times = self.driver.find_elements(by, value)
        for display_time_text in display_times:
            display_time = display_time_text.text
            time_text.append(display_time.split("(")[0].strip())
        return time_text

    def get_time_difference(self, depart, arrival):
        time_format = "%b %d, %I:%M %p"
        depart_time = datetime.strptime(depart, time_format)
        arrival_time = datetime.strptime(arrival, time_format)
        time_difference = arrival_time - depart_time
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds % 3600) // 60

        if minutes == 0:
            formatted_time = f"{hours} Hr"
        else:
            formatted_time = f"{hours} Hr {minutes} Min"
        return formatted_time

    def get_duration(self, duration):
        by, value = duration
        actual_duration = []
        durations = self.driver.find_elements(by, value)
        for duration_text in durations:
            duration = duration_text.text
            split_text = duration.split(":")
            # actual_duration = " ".join(duration.split(" : ")[1].split()).strip()
            actual_duration.append(split_text[1].strip())
        return actual_duration

    def get_display_location(self, location):
        by, value = location
        display_locations = []
        display_location_text = self.driver.find_elements(by, value)
        for display_location in display_location_text:
            display_locations.append(display_location.text)
        return display_locations