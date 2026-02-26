import logging

logger = logging.getLogger(__name__)

class TestGetBookings:
    """
    Suite of tests covering the booking filtering.

    """

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
        assert isinstance(booking_ids, list), "Expected a list of bookings."
        assert len(booking_ids) > 0, "Booking IDs should not be empty."
        if len(booking_ids) > 0:
         assert "bookingid" in booking_ids[0], "Booking object missing 'bookingid' attribute."

    def test_create_and_validate_multiple_bookings(self, booking_service, bookings_payload):
        """
        Test for creating multiple bookings and validating integrity.
        :param booking_service: An instance of Booking service object.
        :param bookings_payload: Test data for multiple bookings creation.
        """
        list_of_bookings = booking_service.create_and_validate_multiple_bookings(bookings_payload)
        assert list_of_bookings is not None, "Failed to create multiple bookings."
        booking_service.get_and_validate_booking_list()
        booking_service.booking_data_cleanup()


    def test_get_booking_ids_by_name_and_surname(self, booking_service, temp_booking):
        """
        Test for checking that booking ids can be filtered by name and surname.
        Steps:
        1. Request all booking IDs by name and surname.
        2. Verify status code and data structure.
        :param booking_service: Booking service object.
        :param temp_booking: Temporary booking service object.
        """
        logger.info("Fetching all booking IDs by name and surname.")
        firstname = temp_booking["booking"]["firstname"]
        lastname = temp_booking["booking"]["lastname"]
        booking_ids = booking_service.get_booking_ids(firstname=firstname, lastname=lastname)
        assert isinstance(booking_ids, list), "Expected a list of bookings."
        if len(booking_ids) > 0:
         assert "bookingid" in booking_ids[0], f"Booking object missing 'bookingid' attribute."

    def test_get_booking_checkin_checkout(self, booking_service, temp_booking):
        """
        Test for checking that booking ids can be filtered by checkin and checkout.
        Steps:
        1. Request all booking checkin IDs.
        2. Verify status code and data structure.
        :param booking_service: Booking service object.
        :param temp_booking: Temporary booking service object.
        """
        checkin = temp_booking["booking"]["bookingdates"]["checkin"]
        checkout = temp_booking["booking"]["bookingdates"]["checkout"]
        booking_ids = booking_service.get_booking_ids(checkin=checkin, checkout=checkout)
        assert isinstance(booking_ids, list), "Expected a list of bookings."
        if len(booking_ids) > 0:
         assert "bookingid" in booking_ids[0], f"Booking object missing 'bookingid' attribute."

    def test_creation_deletion_validations_on_multiple_bookings(self, booking_service, bookings_payload):
        """
        Test for creating multiple bookings and validating deleted booking integrity.
        :param booking_service: An instance of Booking service object.
        :param bookings_payload: Test data with multiple bookings.
        """
        bookings = booking_service.create_multiple_bookings(bookings_payload)
        assert isinstance(bookings, list), "Expected a list of bookings."
        assert len(bookings) == 4, "Failed to create all initial bookings."
        booking_service.delete_and_validate_remaining_bookings_from_booking_list(bookings)
