import pytest
from api_client.requests import Requests
from utils.booking_service import BookingService
from utils.constants import BASE_API_URL
from data.test_data import BOOKING_DATA, UPDATE_BOOKING_DATA
import logging

logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """
    Register custom terminal arguments using Pytest's addoption wrapper.
    :param parser: An instance of the argparse.ArgumentParser class.
    """
    parser.addoption("--username", action="store", default="admin")
    parser.addoption("--password", action="store", default="password123")

@pytest.fixture(scope="session")
def terminal_credential(request):
    """
    Fixture for extracting argparse values and returning them as a dictionary.
    :param request: A build in Pytest fixture that represents the current test context.
    This fixture allows access to the config where all terminal options are kept.
    :return:
    """
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")

    if not username or not password:
        pytest.fail("Please provide both username and password.")

    return {"username": username, "password": password}

@pytest.fixture(scope="function")
def booking_payload():
    """Returns the standard template for creating a booking."""
    return BOOKING_DATA[0]

@pytest.fixture(scope="function")
def bookings_payload():
    """Returns the standard template for creating a multiple bookings payload."""
    return BOOKING_DATA

@pytest.fixture(scope="function")
def update_payload():
    """Returns the data template for updating a booking."""
    return UPDATE_BOOKING_DATA

@pytest.fixture(scope="function")
def booking_service(terminal_credential):
    """
    Provides an authenticated booking service object.
    """
    client = Requests(BASE_API_URL)
    booking_service = BookingService(client)
    logger.info(terminal_credential)
    booking_service.create_api_token(terminal_credential)
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
