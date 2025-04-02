import os

import pytest

from pages.traveler_info_page import TravelerInfoPage
from utils.webdriver_setup import get_driver, open_url
from pages.seat_selection_page import SeatSelectionPage
from pages.trip_search_page import TripSearchPage
from pages.trip_result_page import TripResultPage

@pytest.fixture(scope="session")
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

# @pytest.fixture
# def requested_seat():
#     return 4
# #
# @pytest.fixture
# def expected_max_seat():
#     return 4
#
# @pytest.fixture
# def expected_min_seat():
#     return 1

@pytest.fixture
def seat_page(driver):
    open_url(driver, "https://super-agent-webapp-dev.herokuapp.com/main/trip/3-278253-49-0-4?isForeigner=false&numSeats=4&integrity=95F5B9101C1EE3BC4537BEDE2320BDF22F62C289047500AC270E7333201DC02B")
    return SeatSelectionPage(driver)

@pytest.fixture
def trip_search_page(driver):
    open_url(driver, "https://super-agent-webapp-dev.herokuapp.com/")
    return TripSearchPage(driver)

@pytest.fixture
def trip_result_page(driver):
    open_url(driver, "https://super-agent-webapp-dev.herokuapp.com/main/search?sourceId=Yangon&destinationId=Kyauk+Padaung&departureDate=2025-04-12&numberOfSeats=1&isForeigner=false")
    return TripResultPage(driver)

@pytest.fixture
def traveler_info_page(driver):
    open_url(driver, "https://super-agent-webapp-dev.herokuapp.com/main/traveller/1124?integrity=F263B11B1B3FD9E891CCA324E2D70517B884E83DBF5C283D00079788FD039ECE")
    return TravelerInfoPage(driver)


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """Hook to capture screenshot on test failure"""
#     outcome = yield
#     report = outcome.get_result()
#     if report.failed and "driver" in item.fixturenames:
#         driver = item.funcargs["driver"]
#         screenshot_name = f"screenshots/{item.name}.png"
#         driver.save_screenshot(screenshot_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture a screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.failed and "driver" in item.fixturenames:
        driver = item.funcargs["driver"]

        # Ensure screenshot directory exists
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")

        try:
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")