import time
from time import sleep

import pytest
#
# from pages.trip_search_page import TripSearchPage
# from pages.trip_result_page import TripResultPage
# from pages.seat_selection_page import SeatSelectionPage
# from pages.traveler_info_page import TravelerInfoPage
# from pages.payment_page import PaymentPage
from tests.conftest import trip_search_page, trip_result_page, seat_page, traveler_info_page
from utils import data


@pytest.mark.full_flow
def test_booking_flow(driver, trip_search_page, trip_result_page, seat_page, traveler_info_page, payment_page):
    """Testing the whole complete ticket booking flow"""

    old_url = driver.current_url

    ### TRIP SEARCH PAGE
    trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
    trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)

    trip_search_page.click_element(trip_search_page.depart_date)
    trip_search_page.choose_departure_date(data.year, data.month, data.date)
    trip_search_page.choose_nationality(data.nationality1)

    trip_search_page.click_element(trip_search_page.search_btn)

    # check the search form fields' values in Trip result page are the same with search criteria
    # if there are trips result for search criteria
    try:
        trip_count = trip_search_page.get_count(trip_search_page.trip_count_display)
        print(f"Test Passed : Trip Search Page | {trip_count} trip(s) matched your search criteria. Test passed.\n")

    # if there is no result for search criteria
    except Exception as e:
        print(f"Test Passed : Trip Search Page | There is no result matched with your search criteria.")
        try:
            res_text1, res_text2 = trip_search_page.get_empty_result_texts()
            assert res_text1 == data.trip_res_text1 and res_text2 == data.trip_res_text2, f"Test Failed : Result message is different from specification./ {e}"
            print("Test passed : Trip Search Page | Proper validation message for no trip result is displayed successfully.\n\tThe process stops due to no available trip result.")
            return
        except Exception as e2:
            print(f"Error while fetching empty result texts: {e2}")

    ### TRIP RESULT PAGE
    trip_result_page.wait_for_url_to_change(old_url)
    trip_result_page.wait_for_page_to_load()
    assert trip_result_page.is_page_loaded(), "Test Failed : Trip result page is not loaded properly."

    search_seat_text = trip_result_page.get_data(trip_result_page.request_seat)
    search_seat = search_seat_text.split(" ")[0]

    trip_count, trip_list = trip_result_page.available_trips(trip_result_page.trip_result)
    trip_result_page.get_random_trip(trip_list)

    seat_page_ele = trip_result_page.get_element(trip_result_page.next_page_element)
    assert seat_page_ele.is_displayed() , "Test Failed : The system can't navigated to Seat Selection page."
    print(f"Test passed : Trip Result Page | The system successfully redirect to Seat Selection with valid information.\n")

    ### SEAT SELECTION PAGE
    available_seats = seat_page.get_available_seats()
    for i in range(int(search_seat)):
        seat_page.click_seat(available_seats[i])
        assert "seat-selected" in seat_page.get_seat_class(available_seats[i]), "Test Failed : Seat should be selected."
        print("Test Passed : Seat Selection Page | Selecting available seats.\n")

    seat_page.click_proceed_button()

    ### TRAVELER INFO PAGE
    for key, value in data.traveler_info.items():
        locator = traveler_info_page.get_input_field_locator(key)
        if locator:
            traveler_info_page.fill_info(locator, value)
        else:
            print(f"No locator found for {key}.")
    traveler_info_page.get_random_gender(traveler_info_page.gender)
    traveler_info_page.click_element(traveler_info_page.continue_btn)

    payment_page_ele = traveler_info_page.get_element(traveler_info_page.next_page_ele)
    assert payment_page_ele is True, "Test Failed : The system can't navigated to Payment page."
    print(f"Test passed : Traveler Info Page | The system successfully redirect to Payment page with valid information.\n")

    ### PAYMENT PAGE
    # select Mock Pay from payment list
    payment_page.choose_mock_pay()

    # apply promo code
    payment_page.click_element(payment_page.promo_field)
    payment_page.enter_promo(data.valid_promo, payment_page.promo_box)
    payment_page.click_element(payment_page.apply_btn)
    payment_page.click_element(payment_page.proceed_to_pay_btn)
    # pay with mock pay method
    payment_page.mock_payment(data.mock_pin)

    # redirect to merchant page
    confirm_ele = payment_page.redirect_to_complete()
    assert confirm_ele.is_displayed(), "Test Failed : Can't redirect to complete page."
    print("Test Passed : Payment Page | Payment was successful and redirect to booking complete page.")



