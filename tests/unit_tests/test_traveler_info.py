import time

import pytest
from utils import data


@pytest.mark.parametrize("field_value, locator, expected_message", [
    (data.name, "traveler_name", data.field_validation_msg),
    (data.valid_phone, "phone_number", data.field_validation_msg),
    (None, "gender", data.radio_validation_msg)
])
def test_empty_fields(traveler_info_page, field_value, locator, expected_message):
    """Test validation message for empty fields of traveler info page"""
    if locator == "traveler_name":
        traveler_info_page.click_element(traveler_info_page.continue_btn)
        validation_message = traveler_info_page.get_validation_message(traveler_info_page.traveler_name)

    if locator == "gender":
        traveler_info_page.enter_data(traveler_info_page.traveler_name, data.name)
        traveler_info_page.click_element(traveler_info_page.continue_btn)
        validation_message = traveler_info_page.get_validation_message(traveler_info_page.gender)

    if locator == "phone_number":
        traveler_info_page.enter_data(traveler_info_page.traveler_name, data.name)
        traveler_info_page.get_random_gender(traveler_info_page.gender)
        traveler_info_page.click_element(traveler_info_page.continue_btn)
        validation_message = traveler_info_page.get_validation_message(traveler_info_page.phone_number)

    assert expected_message in validation_message, f"Validation message for {locator} field is incorrect."
    print(f"Test passed : Proper error message is displayed when {locator} field is empty. \n")
    time.sleep(3)


def test_invalid_phone_no(traveler_info_page):
    """Test validation message for entering invalid phone number"""
    traveler_info_page.enter_data(traveler_info_page.traveler_name, data.name)
    traveler_info_page.get_random_gender(traveler_info_page.gender)
    for ph_no in data.invalid_phones:
        traveler_info_page.enter_data(traveler_info_page.phone_number, ph_no)
        traveler_info_page.click_element(traveler_info_page.continue_btn)
        validation_message = traveler_info_page.get_validation_message(traveler_info_page.phone_number)
        assert data.invalid_phone_msg in validation_message, f"Validation message for phono number is incorrect when applying invalid value."
    print(f"Test passed : Proper error message is displayed when invalid value is entered in phone number field.")


numbers = [
    ("abcdefghi", False),
    ("123abc", False),
    ("09428167257", True),
    ("123-@#@#$@#$", False),
    ("0912345", False),
    ("091234567890123", False),
    ("091234532", True)
]
@pytest.mark.parametrize("phone_no, should_be_valid", numbers)
def test_different_phone_no(traveler_info_page, phone_no, should_be_valid):
    """test validation message for entering valid and invalid phone number"""
    traveler_info_page.enter_data(traveler_info_page.traveler_name, data.name)
    traveler_info_page.get_random_gender(traveler_info_page.gender)
    traveler_info_page.enter_data(traveler_info_page.phone_number, phone_no)

    if not should_be_valid:
        traveler_info_page.click_element(traveler_info_page.continue_btn)
        validation_message = traveler_info_page.get_validation_message(traveler_info_page.phone_number)
        assert data.invalid_phone_msg in validation_message, f"Validation message for phono number is incorrect when applying invalid value."
        print(f"Test passed : Proper error message is displayed when invalid value ({phone_no}) is entered in phone number field.")
    else:
        traveler_info_page.click_element(traveler_info_page.continue_btn)
        next_ele = traveler_info_page.get_element(traveler_info_page.next_page_ele)
        assert next_ele is True, f"Expected result : The system should redirect to next page."
        print(f"Test passed : ({phone_no}) is a valid phone number. ")


def test_invalid_email(traveler_info_page):
    """Test validation message for entering invalid email"""
    pass