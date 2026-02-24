import logging

logger = logging.getLogger(__name__)

class TestGetBookings:

    def test_get_booking_ids(self, booking_service):
        """
        Test for fetching all booking IDs.
        Steps:
        1. Request all booking IDs.
        2. Verify data structure.
        :param booking_service: Booking service object.
        """
        logger.info("Fetching all booking IDs.")
        booking_ids = booking_service.get_booking_ids()
        data = booking_ids.json()
        assert isinstance(data, list), "Expected a list of bookings."
        assert len(data) > 0, "Booking IDs should not be empty."
        if data.__len__() > 0:
         assert "bookingid" in data[0], "Booking object missing 'bookingid' attribute."

    def test_get_booking_ids_by_name_and_surname(self, booking_service, booking_payload):
        """
        Test for checking that booking ids can be filtered by name and surname.
        Steps:
        1. Request all booking IDs by name and surname.
        2. Verify status code and data structure.
        :param booking_service: Booking service object.
        :param booking_payload: Test data for filtering booking IDs by name and surname.
        """
        logger.info("Fetching all booking IDs by name and surname.")
        booking_ids = booking_service.get_booking_ids(firstname=booking_payload["firstname"], lastname = booking_payload["lastname"])
        data = booking_ids.json()
        assert isinstance(data, list), "Expected a list of bookings."
        if data.__len__() > 0:
         assert "bookingid" in data[0], f"Booking object missing 'bookingid' attribute."

    def test_get_booking_checkin_checkout(self, booking_service, booking_payload):
        """
        Test for checking that booking ids can be filtered by checkin and checkout.
        Steps:
        1. Request all booking checkin IDs.
        2. Verify status code and data structure.
        :param booking_service: Booking service object.
        :param booking_payload: Test data for filtering booking IDs by checkin and checkout.
        """
        booking_ids = booking_service.get_booking_ids(checkin=booking_payload["bookingdates"]["checkin"], checkout=booking_payload["bookingdates"]["checkout"])
        data = booking_ids.json()
        assert isinstance(data, list), "Expected a list of bookings."
        if data.__len__() > 0:
         assert "bookingid" in data[0], f"Booking object missing 'bookingid' attribute."

