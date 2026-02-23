import pytest
from utils.booking_service import BookingService
from data.test_data import BOOKING_DATA, USER_DATA, UPDATE_BOOKING_DATA

@pytest.fixture(scope="session")
def user_data():
    """Returns static user credentials for authentication."""
    return USER_DATA

@pytest.fixture(scope="function")
def booking_payload():
    """Returns the standard template for creating a booking."""
    return BOOKING_DATA

@pytest.fixture(scope="function")
def update_payload():
    """Returns the data template for updating a booking."""
    return UPDATE_BOOKING_DATA

@pytest.fixture(scope="function")
def booking_service(user_data):
    """
    Provides an authenticated booking service object.
    """
    service = BookingService()
    service.create_api_token(user_data)
    return service

@pytest.fixture(scope="function")
def existing_booking_id(booking_service):

    # Create new booking
    new_booking = booking_service.create_booking(BOOKING_DATA)
    booking_id = new_booking.json()['bookingid']
    yield booking_id
    # Clean up the database
    booking_service.delete_booking(booking_id)
