import re
import time

from utils import data

def test_compare_trip_count_with_display(trip_result_page):
    """check the total count of trips result is the same with display total count"""
    display_trip_count = trip_result_page.get_trip_count(trip_result_page.trip_count_display)
    result_count, result_list = trip_result_page.available_trips(trip_result_page.trip_result)
    assert display_trip_count == result_count, f"Display count {display_trip_count} is different with total result count {result_count}."
    print(f"Test passed : Display count {display_trip_count} and total result count {result_count} are the same.")


# def test_apply_filters(trip_result_page):
#     """check the changes of trips result according to filtering the options"""
#     result_count, result_list = trip_result_page.available_trips(trip_result_page.filter_trip_result)
#     if result_count == 0:
#         display_message = trip_result_page.get_data(trip_result_page.empty_filter_result)
#         assert display_message==data.empty_filter_msg, "Display message for no trips matches with applied filters is incorrect."
#
#     if result_count > 0:


def test_seat_count(trip_result_page):
    """check whether the search seat count and displayed seat count are the same or not"""
    random_seat = trip_result_page.random_seat_number(data.expected_min_seat, data.expected_max_seat)
    while random_seat > 1:
        trip_result_page.click_element(trip_result_page.plus_btn)
        random_seat -= 1
    time.sleep(3)
    trip_result_page.click_element(trip_result_page.search_btn)
    time.sleep(3)
    display_seat, price = trip_result_page.get_display_seat_or_price(trip_result_page.display_seat_price)
    print("display seat: ", display_seat)
    search_seat = trip_result_page.get_data(trip_result_page.request_seat)
    print("searched seat: ", search_seat)
    for i in range(len(display_seat)):
        assert display_seat[i] == search_seat, f"The display seat count on the card is different with searched seat count in trip position {i}. "
    print("Test passed : The display seat count in all available trips are the same with searched seat count.")


def test_ticket_amount_check(trip_result_page):
    """check total ticket amount is correct or not according to seat count"""
    random_seat = trip_result_page.random_seat_number(data.expected_min_seat, data.expected_max_seat)
    while random_seat > 1:
        trip_result_page.click_element(trip_result_page.plus_btn)
        random_seat -= 1
    trip_result_page.click_element(trip_result_page.search_btn)
    result_count, result_list = trip_result_page.available_trips(trip_result_page.trip_result)
    print("result count : ", result_count)
    display_seat_text, price = trip_result_page.get_display_seat_or_price(trip_result_page.display_seat_price)
    display_seat = []
    for i in range(len(display_seat_text)):
        seat_count = re.search(r'(\d)', display_seat_text[i]).group(1)
        display_seat.append(seat_count)
    print('Display seat digit : ', display_seat)
    print("Display price : ", price)
    total_amount = trip_result_page.get_total_amount(trip_result_page.total_amt)
    print("Amount list : ", total_amount)

    for i in range(result_count):
       assert int(display_seat[i]) * int(price[i].replace(',', '')) == int(total_amount[i].replace(',', '')), f"The Total ticket amount is different in trip position {i}. "
    print(f"Test passed : All the total ticket amounts are correct according to seat count.")


def test_check_locations_are_same(trip_result_page):
    """check the displayed source and destination on trip result is same with search locations"""
    result_count, result_trip = trip_result_page.available_trips(trip_result_page.trip_result)
    search_source = trip_result_page.get_data(trip_result_page.source_dropdown_text)
    search_destination = trip_result_page.get_data(trip_result_page.destination_dropdown_text)
    display_source = trip_result_page.get_display_location(trip_result_page.display_source)
    display_destination = trip_result_page.get_display_location(trip_result_page.display_destination)

    for i in range(result_count):
        assert search_source==display_source[i] and search_destination==display_destination[i], f"Search data and displayed date are different at trip number {i+1}."
    print("Test passed : Search locations and displayed locations are the same for available trips.")


def test_time_different_for_duration(trip_result_page):
    """check departure and arrival time difference is the same with estimated duration"""
    result_count, result_trip = trip_result_page.available_trips(trip_result_page.trip_result)
    display_duration = trip_result_page.get_duration(trip_result_page.display_duration)
    display_depart = trip_result_page.get_depart_arrival_time(trip_result_page.display_depart_time)
    display_arrival =trip_result_page.get_depart_arrival_time(trip_result_page.display_arrival_time)
    for i in range(result_count):
        time_difference = trip_result_page.get_time_difference(display_depart[i], display_arrival[i])
        assert time_difference == display_duration[i], f"Depart and arrival time difference is not the same with display duration at trip number {i+1}."

    print("Test passed : Departure and arrival time difference are the same with displayed duration for all the trips.")

