from api_client.requests import Requests
from utils.constants import BASE_API_URL, DEFAULT_JSON_HEADERS
import logging

logger = logging.getLogger(__name__)

class BookingService(Requests):
    """
    Service class to handle all interactions with the Booking API.
    Inherits from Requests client.
    """
    def __init__(self):
        """
        Init the Service class.
        """
        super().__init__(base_url=BASE_API_URL, headers=DEFAULT_JSON_HEADERS)

    @staticmethod
    def _handle_response(response, expected_status):
        logger.info("Verifying status code matches expected status code.")
        if response.status_code != expected_status:
            raise AssertionError(f"Expected status code {expected_status}, received {response.status_code}")
        return response

    def create_api_token(self, test_user: dict) ->str:
        """
        Create an API token for the Booking API.
        :param test_user: Dictionary with test user username and password.
        :return: The authentication token for the Booking API.
        """
        path = "/auth"
        response = self.post(path, json=test_user)
        if response.status_code == 200:
            token = response.json().get("token")
            self.session.headers.update({"Cookie": f"token={token}"})
            return token
        return ""

    def get_booking_ids(self, **params):
        """
        Get all booking ids.
        :param params: Optional parameters for filtering booking ids.
        :return: A list of booking ids.
        """
        path = "/booking"
        booking_ids_response = self.get(path, params=params)
        return self._handle_response(booking_ids_response, 200)

    def get_booking(self, booking_id: int):
        """
        Get a specific booking details.
        :param booking_id: The unique booking id to get.
        :return: Dictionary with booking details.
        """
        path = f"/booking/{booking_id}"
        booking = self.get(path)
        return self._handle_response(booking, 200)

    def create_booking(self, booking_data: dict):
        """
        Create a new booking.
        :param booking_data: Dictionary with booking details.
        :return: Dictionary of created booking details.
        """
        path = "/booking"
        new_booking = self.post(path, json=booking_data)
        return self._handle_response(new_booking, 200)

    def update_booking(self, booking_id: int, booking_data: dict) -> dict:
        """
        Update a booking details.
        :param booking_id: The unique booking id to update.
        :param booking_data: The new booking details.
        :return: The updated booking details.
        """
        path = f"/booking/{booking_id}"
        update_response = self.patch(path, json=booking_data)
        return self._handle_response(update_response, 200)

    def update_booking_partial(self, booking_id: int, booking_data: dict) -> dict:
        """
        Update a booking partial details.
        :param booking_id: The unique booking id to update.
        :param booking_data: The specific fields to update.
        :return: The updated booking details.
        """
        path = f"/booking/{booking_id}"
        partial_update_response = self.patch(path, json=booking_data)
        return self._handle_response(partial_update_response, 200)

    def delete_booking(self, booking_id: int):
        """
        Delete a booking details.
        :param booking_id: The unique booking id to delete.
        :return: Status string 'Created'
        """
        path = f"/booking/{booking_id}"
        delete_response = self.delete(path)
        return self._handle_response(delete_response, 201)

    def health_check(self):
        """
        Health check endpoint.
        :return: Status string 'Created'
        """
        path ="/ping"
        ping_response = self.get(path)
        return self._handle_response(ping_response, 200)
