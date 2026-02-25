import pytest
from api_client.requests import Requests
from utils.booking_service import BookingService
from utils.constants import BASE_API_URL
from data.test_data import BOOKING_DATA, USER_DATA, UPDATE_BOOKING_DATA
import logging

logger = logging.getLogger(__name__)

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

@pytest.fixture(scope="function")
def temp_booking(booking_service, booking_payload):
    """
    Creates a new booking specifically for testing.
    :param booking_service: An instance of the BookingService class.
    :param booking_payload: The payload for the booking.
    :return: Created booking object.
    """
    logging.info("Setup: Creating a temp booking.")
    response = booking_service.create_booking(booking_payload)
    yield response

    logger.info("Teardown: Deleting a temp booking.")
    booking_service.delete_booking(response["bookingid"])
