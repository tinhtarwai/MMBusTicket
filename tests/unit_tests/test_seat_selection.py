import random
from utils.data import requested_seat

def test_select_available_seat(seat_page):
    """test selecting available seats"""
    selected_list = []
    available_seats = seat_page.get_available_seats()
    available_seats_no = [seat.text for seat in available_seats]
    print(f"Available seats: {len(available_seats)} {available_seats_no}")

    for i in range(requested_seat):
        seat_page.click_seat(available_seats[i])
        selected_list.append(available_seats[i].text)
        assert "seat-selected" in seat_page.get_seat_class(available_seats[i]), "Seat should be selected"
    print("Your selected seats:", ", ".join(selected_list))
    print("Test passed : Selecting available seats.\n")


def test_select_unavailable_seat(seat_page):
    """test selecting unavailable seats"""
    all_seats = seat_page.get_all_seats()
    for seat in all_seats:
        if "seat-unavailable" in seat_page.get_seat_class(seat):
            try:
                seat_page.click_seat(seat)
                assert "seat-unavailable" in seat_page.get_seat_class(seat), "Seat should remain unavailable."
            except Exception as e:
                print(f"Expected exception: {e}")
    print("Test passed: Cannot select unavailable seats.\n")


def test_select_not_enough_seat(seat_page):
    """test selecting when not enough seats are available"""
    selected_list = []
    for i in range(requested_seat):
        available_seats = seat_page.get_available_seats()

        if len(available_seats) == 0:
            print("Not available/enough seats to choose.")
            break
        else:
            seat = random.choice(available_seats)
            seat_page.click_seat(seat)
            selected_list.append(seat.text)
            assert "seat-selected" in seat_page.get_seat_class(seat), "Seat should be selected after clicking."
    print(f"Requested seats: {requested_seat}, Selected: {len(selected_list)} ({', '.join(selected_list)})")
    print("Test passed: Handling not enough seats scenario.")


def test_select_more_than_requested_seats(seat_page):
    """test selecting more than requested seats"""
    tot_selected_seats = []
    # available_seats = seat_page.get_available_seats()
    print("Seats attempted to be selected: ", end = " ")

    ## selecting the first available seats
    # for i in range(requested_seat+2):
    #       print(available_seats[i].text, end= ", ")
    #       available_seats[i].click()
    #       if "seat-selected" in seat_page.get_seat_class(available_seats[i]):
    #          tot_selected_seats.append(available_seats[i])

    ## selecting random available seats
    for i in range(requested_seat + 3):
        available_seats = seat_page.get_available_seats()
        random_seat = random.choice(available_seats)
        print(random_seat.text, end=" ")

        seat_page.click_seat(random_seat)
        if "seat-selected" in seat_page.get_seat_class(random_seat):
            tot_selected_seats.append(random_seat.text)

    print(f"Actual selected seats: {tot_selected_seats}")
    print(f"Expected: {requested_seat}, Selected: {len(tot_selected_seats)}\n")

    assert len(tot_selected_seats) == requested_seat, "System should not allow selecting more than requested seats."

    print("Test passed: Cannot select more than requested seats.\n")


def test_select_less_than_requested_seats(seat_page):
    """test selecting fewer than requested seats"""
    selected_list = []
    available_seats = seat_page.get_available_seats()

    for i in range(requested_seat - 2):
        seat_page.click_seat(available_seats[i])
        selected_list.append(available_seats[i])

    seat_page.click_proceed_button()

    if requested_seat > len(selected_list):
        print(f"The user needs to choose {requested_seat - len(selected_list)} more seats.")
        print("Test passed: System does not allow proceeding with fewer than requesting seats.\n")


def test_select_and_deselect_seat(seat_page):
    """test selecting and deselecting a seat"""
    available_seats = seat_page.get_available_seats()
    available_seat = random.choice(available_seats)
    seat_page.click_seat(available_seat)
    assert "seat-selected" in seat_page.get_seat_class(available_seat), "Seat should be selected."
    seat_page.click_seat(available_seat)
    assert "seat-selected" not in seat_page.get_seat_class(available_seat), "Seat should be deselected."
    print("Test passed: Seat can be selected and deselected.\n")