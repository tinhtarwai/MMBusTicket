# import time
# import pytest
# from utils import data
#
# ### JUST FOR CODE REFERENCE ###
#
# @pytest.mark.parametrize("field, locator, expected_message", [
#     ("source", "source_dropdown", data.location_validation_msg),
#     ("destination", "destination_dropdown", data.location_validation_msg),
#     ("departure_date", None, data.date_validation_msg)
# ])
#
# def test_empty_fields(trip_search_page, field, locator, expected_message):
#     """Test Validation message for empty source, destination and departure date"""
#     if field == "source":
#         trip_search_page.click_element(trip_search_page.search_btn)
#         validation_message = trip_search_page.get_validation_message(trip_search_page.source_dropdown)
#
#     elif field == "destination":
#         trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
#         trip_search_page.click_element(trip_search_page.search_btn)
#         validation_message = trip_search_page.get_validation_message(trip_search_page.destination_dropdown)
#
#     elif field == "departure_date":
#         trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
#         trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)
#         trip_search_page.click_element(trip_search_page.search_btn)
#         validation_message = trip_search_page.get_form_validation_message()
#
#     assert validation_message == expected_message, f"Validation message for {field} field is incorrect."
#     print(f"Test passed : Proper error message is displayed when {field} field is empty. \n")
#
# # def test_empty_source(trip_search_page):
# #     """test for empty value in source location"""
# #     trip_search_page.click_element(trip_search_page.search_btn)
# #     validation_message = trip_search_page.get_validation_message(trip_search_page.source_dropdown)
# #     assert validation_message == data.location_validation_msg, "Validation message is different with specification."
# #     print("Test passed : Proper error message is displayed when source location field is empty.\n")
# #
# # def test_empty_destination(trip_search_page):
# #     """test for empty value in destination location"""
# #     trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
# #     trip_search_page.click_element(trip_search_page.search_btn)
# #     validation_message = trip_search_page.get_validation_message(trip_search_page.destination_dropdown)
# #     assert validation_message == data.location_validation_msg, "Validation message is different with specification."
# #     print("Test passed : Proper error message is displayed when destination location field is empty.\n")
# #
# # def test_empty_departure_date(trip_search_page):
# #     """test for empty value in departure date"""
# #     trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
# #     trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)
# #     trip_search_page.click_element(trip_search_page.search_btn)
# #     validation_message = trip_search_page.get_form_validation_message()
# #     assert validation_message == data.date_validation_msg, "Validation message is different with specification."
# #     print("Test passed : Proper error message is displayed when departure date field is empty.\n")
#
# @pytest.mark.parametrize("location, locator, empty_result_locator", [
#     (data.invalid_source_loc, "source" , "empty_result_source"),
#     (data.invalid_destination_loc, "destination", "empty_result_destination")
# ])
# def test_invalid_inputs(trip_search_page, location, locator, empty_result_locator):
#     """check for invalid input in source or destination fields"""
#     trip_search_page.enter_location(location, getattr(trip_search_page,locator), trip_search_page.search_field)
#     empty_result = trip_search_page.get_location_empty_result(getattr(trip_search_page, empty_result_locator))
#     assert empty_result == data.empty_result, "Message for no result is incorrect."
#     # to close from dropdown, try click on hero banner text
#     trip_search_page.click_element(trip_search_page.focus_click)
#     print(f"Test passed: Proper validation message displayed for invalid input in '{locator}' field.\n")
#
# # def test_invalid_input(trip_search_page):
# #     """check for invalid input in source or destination fields"""
# #     trip_search_page.enter_location(data.invalid_source_loc, trip_search_page.source, trip_search_page.search_field)
# #     from_empty_result = trip_search_page.get_location_empty_result(trip_search_page.empty_result_source)
# #     assert from_empty_result == data.empty_result, "Message for no result is different with specification."
# #     # to close from dropdown, try click on hero banner text
# #     trip_search_page.click_element(trip_search_page.focus_click)
# #     trip_search_page.enter_location(data.invalid_destination_loc, trip_search_page.destination, trip_search_page.search_field)
# #     to_empty_result = trip_search_page.get_location_empty_result(trip_search_page.empty_result_destination)
# #     assert to_empty_result == data.empty_result, "Message for no result is different with specification."
# #     print("Test passed : Proper validation message is displayed for no result matched with search keyword.\n")
#
# def test_not_choosing_nationality(trip_search_page):
#     """test for not choosing Nationality field"""
#     trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
#     trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)
#     trip_search_page.click_element(trip_search_page.depart_date)
#     trip_search_page.choose_departure_date(data.year, data.month, data.date)
#     time.sleep(2)
#     trip_search_page.click_element(trip_search_page.search_btn)
#     time.sleep(1)
#     validation_msg = trip_search_page.get_form_validation_message()
#     assert validation_msg == data.nationality_validation_msg, "Validation message is different with specification."
#     print("Test passed : Proper error message is displayed for not choosing nationality.\n")
#
#
# @pytest.mark.parametrize("action, button, expected_seat_count", [
#     ("max", "plus_seat_btn", data.expected_max_seat),
#     ("min", "minus_seat_button", data.expected_min_seat)
# ])
#
# def test_seat_selection_count(trip_search_page, action, button, expected_seat_count):
#     """check the maximum and minimum count of seats."""
#     while not trip_search_page.get_element_disabled(trip_search_page.plus_seat_btn):
#         trip_search_page.click_element(trip_search_page.plus_seat_btn)
#
#     if action== "min":
#         while not trip_search_page.get_element_disabled(trip_search_page.minus_seat_btn):
#             trip_search_page.click_element(trip_search_page.minus_seat_btn)
#
#     seat_count = trip_search_page.get_count(trip_search_page.seat_display)
#
#     assert seat_count == expected_seat_count, f"{action.capitalize()} seat count is different with system's specification."
#     print(f"{action.capitalize()} seat count {seat_count} matches with system's specification.\n")
#
# # def test_max_seat_count(trip_search_page):
# #     """check the maximum count of seat"""
# #     while not trip_search_page.get_element_disabled(trip_search_page.plus_seat_btn):
# #         trip_search_page.click_element(trip_search_page.plus_seat_btn)
# #     seat_count = trip_search_page.get_count(trip_search_page.seat_display)
# #     assert seat_count == data.expected_max_seat, f"Maximum seat count {seat_count} is not the same with system's specification."
# #     print(f"Test passed : Maximum seat count {seat_count} is the same with system's specification.\n")
#
# # def test_min_seat_count(trip_search_page):
# #     """check the minimum count of seat"""
# #     while not trip_search_page.get_element_disabled(trip_search_page.plus_seat_btn):
# #         trip_search_page.click_element(trip_search_page.plus_seat_btn)
# #     while not trip_search_page.get_element_disabled(trip_search_page.minus_seat_btn):
# #         trip_search_page.click_element(trip_search_page.minus_seat_btn)
# #     seat_count = trip_search_page.get_count(trip_search_page.seat_display)
# #     assert seat_count == data.expected_min_seat, f"Minimum seat count {seat_count} is not the same with system's specification."
# #     print(f"Test passed : Minimum seat count {seat_count} is the same with system's specification.\n")
# #
#
# def test_choose_same_location(trip_search_page):
#     """check for selecting same location in source and destination fields"""
#     #try selecting the same source location in destination field
#     trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
#     source_loc = trip_search_page.get_location_text(trip_search_page.source_dropdown_text)
#     print("Selected source location :", source_loc)
#     trip_search_page.click_element(trip_search_page.destination)
#     time.sleep(1)
#     disabled_destination_loc = trip_search_page.get_disabled_location_text(trip_search_page.disabled_destination)
#     print("Disabled destination location: ", disabled_destination_loc)
#     if source_loc in disabled_destination_loc:
#         is_disabled = trip_search_page.get_element_disabled(trip_search_page.disabled_destination)
#         assert is_disabled == True, "Test failed : Same location is still clickable."
#         try:
#             disabled_destination_loc.click()
#             print("Test failed : Same location is still clickable.\n")
#         except Exception as e:
#             print("Test Passed: Same location in Destination field is disabled and not clickable.")
#
#     trip_search_page.clear_locations(trip_search_page.source_dropdown, trip_search_page.destination_dropdown)
#
#     # try selecting the same destination location in source field
#     trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)
#     destination_loc = trip_search_page.get_location_text(trip_search_page.destination_dropdown_text)
#     print("Selected destination location :", destination_loc)
#     trip_search_page.select_location(data.destination_location, trip_search_page.source_dropdown)
#     time.sleep(1)
#     source_loc = trip_search_page.get_location_text(trip_search_page.source_dropdown_text)
#     print("Selected source location :", source_loc)
#     muted_destination = trip_search_page.is_destination_muted(trip_search_page.muted_destination)
#     assert muted_destination == "To", "Something went wrong"
#     print("Test passed : The selected destination location is clear and only placeholder text 'To' is displayed")
#
# @pytest.mark.parametrize("year, month, date, nationality", [
#     (data.year, data.month, data.date, data.nationality1),
#     (data.year, data.month1, data.date1, data.nationality2)
# ])
#
# def test_search_with_valid_inputs(trip_search_page, year, month, date, nationality):
#     """check for searching with valid inputs"""
#     trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
#     trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)
#     trip_search_page.click_element(trip_search_page.depart_date)
#     trip_search_page.choose_departure_date(year, month, date)
#     trip_search_page.choose_nationality(nationality)
#     time.sleep(1)
#     trip_search_page.click_element(trip_search_page.search_btn)
#     # check the search form fields' values in Trip result page are the same with search criteria
#     # if there are trips result for search criteria
#     try:
#         trip_count = trip_search_page.get_count(trip_search_page.trip_count_display)
#         print(f"{trip_count} trip(s) matched your search criteria. Test passed.\n")
#
#     # if there is no result for search criteria
#     except Exception as e:
#         print("There is no result matched with your search criteria.")
#         try:
#             res_text1, res_text2 = trip_search_page.get_empty_result_texts()
#             assert res_text1 == data.trip_res_text1 and res_text2 == data.trip_res_text2, f"Result message is different from specification./ {e}"
#             print("Test passed : Proper validation message for no trip result is displayed successfully.\n")
#         except Exception as e2:
#             print(f"Error while fetching empty result texts: {e2}")
#     time.sleep(2)
#
# # def test_search_with_valid_input(trip_search_page):
# #     """check for searching with valid inputs"""
# #     trip_search_page.select_location(data.source_location, trip_search_page.source_dropdown)
# #     trip_search_page.select_location(data.destination_location, trip_search_page.destination_dropdown)
# #     trip_search_page.click_element(trip_search_page.depart_date)
# #     trip_search_page.choose_departure_date(data.year, data.month, data.date)
# #     trip_search_page.choose_nationality(data.nationality1)
# #     time.sleep(1)
# #     trip_search_page.click_element(trip_search_page.search_btn)
# #     # check the search form fields' values in Trip result page are the same with search criteria
# #     # if there are trips result for search criteria
# #     try:
# #         trip_count = trip_search_page.get_count(trip_search_page.trip_count_display)
# #         print(f"{trip_count} trip(s) matched your search criteria. Test passed.\n")
# #
# #     # if there is no result for search criteria
# #     except Exception as e:
# #         print("There is no result matched with your search criteria.")
# #         try:
# #             res_text1, res_text2 = trip_search_page.get_empty_result_texts()
# #             assert res_text1 == data.trip_res_text1 and res_text2 == data.trip_res_text2, f"Result message is different from specification./ {e}"
# #             print("Test passed : Proper validation message for no trip result is displayed successfully.\n")
# #         except Exception as e2:
# #             print(f"Error while fetching empty result texts: {e2}")