import pytest
from api_client.requests import Requests
from utils.booking_service import BookingService
from utils.constants import BASE_API_URL
from data.test_data import BOOKING_DATA, USER_DATA, UPDATE_BOOKING_DATA

@pytest.fixture(scope="function")
def booking_payload():
    """Returns the standard template for creating a booking."""
    return BOOKING_DATA

@pytest.fixture(scope="function")
def update_payload():
    """Returns the data template for updating a booking."""
    return UPDATE_BOOKING_DATA

@pytest.fixture(scope="function")
def booking_service():
    """
    Provides an authenticated booking service object.
    """
    client = Requests(BASE_API_URL)
    booking_service = BookingService(client)
    booking_service.create_api_token(USER_DATA)
    return booking_service
