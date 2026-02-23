from api_client.requests import Requests
from utils.constants import BASE_API_URL, DEFAULT_JSON_HEADERS

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
        return self.get(path, params=params)

    def get_booking(self, booking_id: int):
        """
        Get a specific booking details.
        :param booking_id: The unique booking id to get.
        :return: Dictionary with booking details.
        """
        path = f"/booking/{booking_id}"
        return self.get(path)

    def create_booking(self, booking_data: dict):
        """
        Create a new booking.
        :param booking_data: Dictionary with booking details.
        :return: Dictionary of created booking details.
        """
        path = "/booking"
        return self.post(path, json=booking_data)

    def update_booking(self, booking_id: int, booking_data: dict) -> dict:
        """
        Update a booking details.
        :param booking_id: The unique booking id to update.
        :param booking_data: The new booking details.
        :return: The updated booking details.
        """
        path = f"/booking/{booking_id}"
        return self.put(path, json=booking_data)

    def update_booking_partial(self, booking_id: int, booking_data: dict) -> dict:
        """
        Update a booking partial details.
        :param booking_id: The unique booking id to update.
        :param booking_data: The specific fields to update.
        :return: The updated booking details.
        """
        path = f"/booking/{booking_id}"
        return self.patch(path, json=booking_data)

    def delete_booking(self, booking_id: int):
        """
        Delete a booking details.
        :param booking_id: The unique booking id to delete.
        :return: Status string 'Created'
        """
        path = f"/booking/{booking_id}"
        return self.delete(path)

    def health_check(self):
        """
        Health check endpoint.
        :return: Status string 'Created'
        """
        path ="/ping"
        return self.get(path)
