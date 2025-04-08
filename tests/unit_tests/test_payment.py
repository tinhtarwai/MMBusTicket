import time

from utils import data

invalid_codes = ["123456", "tdg3500"]
def test_apply_invalid_promo(payment_page):
    """Test validation message for applying invalid promo code"""
    payment_page.get_random_payment()
    payment_page.click_element(payment_page.promo_field)
    for code in invalid_codes:
        payment_page.enter_promo(code, payment_page.promo_box)
        time.sleep(2)
        payment_page.click_element(payment_page.apply_btn)
        time.sleep(2)
        error_msg = payment_page.get_validation_message()
        print(f"display error message for {code} : {error_msg}")
        assert error_msg == data.invalid_promo_msg, "Failed: validation message for applying invalid promo code is incorrect."
        print("Test Passed : Proper validation message is displayed for applying invalid promo code.")


def test_apply_empty_promo(payment_page):
    """Test validation message for applying empty promo code"""
    payment_page.get_random_payment()
    payment_page.click_element(payment_page.promo_field)
    time.sleep(1)
    payment_page.click_element(payment_page.apply_btn)
    time.sleep(3)
    empty_msg = payment_page.get_validation_message()
    print("display error message : ", empty_msg)
    assert empty_msg == data.empty_promo_msg, "Failed: validation message for applying empty promo code is incorrect."
    print("Test Passed : Proper validation message is displayed for applying empty promo code.")

def test_apply_valid_promo(payment_page):
    """Test applying valid promo code and check the amount"""
    payment_page.get_random_payment()
    payment_page.click_element(payment_page.promo_field)
    payment_page.enter_promo(data.valid_promo, payment_page.promo_box)
    payment_page.click_element(payment_page.apply_btn)
    time.sleep(2)
    calculated_total = payment_page.get_total_calculation()
    display_total = payment_page.get_total_amount(payment_page.total)
    assert int(calculated_total) == int(display_total), "Test failed : The display total amount is different with calculation."
    print("Test passed : Display total amount is the same with calculated amount after applying promo code." )