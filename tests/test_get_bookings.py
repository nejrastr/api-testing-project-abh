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

    def test_delete_integrity(self, booking_service, booking_payload):
        """
        Test for validating deleted booking integrity.
        :param booking_service: An instance of Booking service object.
        :param booking_payload: Booking data payload object.
        """
        bookings = booking_service.create_multiple_bookings(booking_payload)
        assert isinstance(bookings, list), "Expected a list of bookings."
        assert len(bookings) == 4, "Failed to create all initial bookings."

        booking_to_delete = bookings[1]["bookingid"]
        bookings_to_keep = [b for b in bookings if b["bookingid"] != booking_to_delete]

        logger.info(f"Deleting booking {booking_to_delete}")
        booking_service.delete_booking(booking_to_delete, 201)
        logger.info(f"Verify booking {booking_to_delete} was deleted.")
        booking_service.get_booking(booking_to_delete, 404)

        for expected_booking in bookings_to_keep:
            keep_id = expected_booking["bookingid"]
            original_booking = expected_booking["booking"]

            logger.info(f"Verifying integrity for remaining booking: {keep_id}")
            remaining_booking = booking_service.get_booking(keep_id, 200)
            booking_service.validate_data(original_booking, remaining_booking)
