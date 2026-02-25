from utils.constants import BASE_API_URL, DEFAULT_JSON_HEADERS
import logging
from api_client.requests import Requests

logger = logging.getLogger(__name__)

class BookingService:
    """
    Service class to handle all interactions with the Booking API.
    Inherits from Requests client.
    """
    def __init__(self, client: Requests):
        """
        Init the Service class.
        """
        self.client = client
        self.client.base_url = BASE_API_URL
        self.client.session.headers.update(DEFAULT_JSON_HEADERS)

    @staticmethod
    def _handle_response(response, expected_status):
        """
        Internal helper method to validate status codes.
        :param response: Response from API.
        :param expected_status: Expected status code from API.
        :return:
        """
        logger.info("Verifying status code matches expected status code.")
        if response.status_code != expected_status:
            raise AssertionError(f"Expected status code {expected_status}, received {response.status_code}")
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
        return response.text

    def create_api_token(self, test_user: dict, expected_status = 200) ->str:
        """
        Create an API token for the Booking API.
        :param expected_status: Expected status code from API.
        :param test_user: Dictionary with test user username and password.
        :return: The authentication token for the Booking API.
        """
        path = "/auth"
        response = self.client.post(path, json=test_user)
        self._handle_response(response, expected_status)
        token = response.json()['token']
        if token:
            self.client.session.headers.update({"Cookie": f"token={token}"})
            logger.info("Successfully added auth token to API headers.")
            return token
        raise ValueError("Token not added to API headers.")

    def get_booking_ids(self, expected_status = 200,**params):
        """
        Get all booking ids.
        :param expected_status: Expected status code from API.
        :param params: Optional parameters for filtering booking ids.
        :return: A list of booking ids.
        """
        path = "/booking"
        booking_ids_response = self.client.get(path, params=params)
        return self._handle_response(booking_ids_response, expected_status)

    def get_booking(self, booking_id: int, expected_status = 200):
        """
        Get a specific booking details.
        :param expected_status: Expected status code from API.
        :param booking_id: The unique booking id to get.
        :return: Dictionary with booking details.
        """
        path = f"/booking/{booking_id}"
        booking = self.client.get(path)
        return self._handle_response(booking, expected_status)

    def get_and_validate_booking(self, booking_id: int, booking_payload: dict):
        """
        Method to get and validate a booking details.
        :param booking_id: Booking ID.
        :param booking_payload: Test booking data.
        """
        booking = self.get_booking(booking_id)
        self.validate_data(booking ,booking_payload)
        return booking

    def create_booking(self, booking_data: dict, expected_status = 200):
        """
        Create a new booking.
        :param expected_status: Expected status code from API.
        :param booking_data: Dictionary with booking details.
        :return: Dictionary of created booking details.
        """
        path = "/booking"
        new_booking = self.client.post(path, json=booking_data)
        return self._handle_response(new_booking, expected_status)

    def update_booking(self, booking_id: int, booking_data: dict, partial = False, expected_status = 200) -> dict:
        """
        Update a booking details partially or fully based on flag partial.
        :param booking_id: ID of the booking to update.
        :param booking_data: Booking details to update.
        :param partial: Flag to indicate whether to update partially.
        :param expected_status: Expected status code from API.
        :return: dictionary with updated booking details.
        """
        method = self.client.patch if partial else self.client.put
        path = f"/booking/{booking_id}"
        update_response = method(path, json=booking_data)
        return self._handle_response(update_response, expected_status)

    def update_and_validate_booking(self, booking_id: int, update_booking_data: dict, partial = False):
        """
        Method to update and validate a booking details.
        :param booking_id: Booking ID.
        :param update_booking_data: Test data for updating booking details.
        :param partial: Flag to indicate whether to update partially or fully.
        :return: Updated booking object.
        """
        updated_booking = self.update_booking(booking_id, update_booking_data, partial)
        self.validate_data(updated_booking, update_booking_data)
        return updated_booking


    def delete_booking(self, booking_id: int, expected_status = 201):
        """
        Delete a booking details.
        :param expected_status: Expected status code from API.
        :param booking_id: The unique booking id to delete.
        :return: Status string 'Created'
        """
        path = f"/booking/{booking_id}"
        logger.info(f"Headers before delete: {self.client.session.headers}")
        delete_response = self.client.delete(path)
        return self._handle_response(delete_response, expected_status)

    def health_check(self, expected_status = 200):
        """
        Health check endpoint.
        :return: Status string 'Created'
        """
        path ="/ping"
        ping_response = self.client.get(path)
        return self._handle_response(ping_response, expected_status)

    @staticmethod
    def validate_data(actual_data, expected_data):
        """
        Method to validate the data passed.
        :param actual_data: Data that is returned from the API.
        :param expected_data: Test data that is expected to be returned from the API.
        :return:
        """
        for key, value in expected_data.items():
            assert actual_data[key] == value, (
                f"Data mismatch for key '{key}': "
                f"Expected {value}, but got {actual_data[key]}"
            )

    def create_and_validate_booking(self, booking_payload: dict):
        """
        Method for booking creation and validation.
        Steps:
        1. Create a new booking.
        2. Validate that booking response contains bookingid
        3. Validate booking response data
        4. Fetch new booking by bookingid from GET endpoint.
        5. Validate that data returned from GET endpoint matches expected data.
        :param booking_payload:
        :return:
        """
        logger.info(f"Creating new booking: {booking_payload}")
        created_booking = self.create_booking(booking_payload)

        logger.info("Verifying booking response contains booking id.")
        assert "bookingid" in created_booking, "Booking response does not contain 'bookingid' attribute."
        logger.info("Verifying that returned data from response matches expected data.")
        self.validate_data(created_booking["booking"], booking_payload)
        logger.info("Fetching booking details from API endpoint by newly created booking id.")
        new_id = created_booking["bookingid"]
        new_booking = self.get_booking(new_id)
        logger.info(
            f"Verifying that returned data from API endpoint matches submitted data, newly created booking data: {new_booking}")
        self.validate_data(new_booking, booking_payload)
        return new_id

    def create_multiple_bookings(self, booking_payload: list):
        """
        Method for creating multiple bookings.
        :param booking_payload: Test data with multiple bookings.
        """
        return [self.create_booking(booking) for booking in booking_payload]
