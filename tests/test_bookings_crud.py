import logging
from conftest import booking_service

logger = logging.getLogger(__name__)

class TestBookingActions:
    """
    Suite of tests covering the CRUD operations related to booking actions.
    """
    def test_create_booking(self, booking_service, booking_payload):
        """
        Test for creating and validating booking.
        :param booking_service: An instance of BookingService.
        :param booking_payload: Booking service test data.
        """
        booking_id = booking_service.create_and_validate_booking(booking_payload)
        booking_service.set_test_data("shared_booking_id", booking_id)
        assert booking_id is not None

    def test_get_booking(self, booking_service, booking_payload):
        """
        Test for fetching booking data by id.
        Steps:
        1. Fetch booking details by booking id.
        :param booking_service: An instance of BookingService.
        """
        target_id = booking_service.get_test_data("shared_booking_id")
        assert target_id is not None
        logger.info("Fetch booking details by booking id.")
        booking_service.get_and_validate_booking(target_id, booking_payload)


    def test_update_booking(self, booking_service, update_payload):
       """
       Test for updating booking.
       Steps:
       1. Update booking by existing booking id.
       2. Verify status code and data structure.
       :param booking_service: An instance of BookingService.
       :param update_payload: Test data for updating booking.
       """
       target_id = booking_service.get_test_data("shared_booking_id")
       assert target_id is not None
       logger.info(f"Updating booking: {update_payload}")
       booking_service.update_and_validate_booking(target_id, update_payload)

    def test_delete_booking(self, booking_service, booking_payload):
        """
        Steps:
        1. Delete booking by booking id.
        2. Verify that booking is deleted from database successfully.

        """
        target_id = booking_service.get_test_data("shared_booking_id")
        assert target_id is not None
        logger.info("Deleting temp booking...")
        booking_service.delete_booking(target_id)
        logger.info("Verifying that booking is successfully deleted from database.")
        booking_service.get_booking(target_id, 404)

    def test_booking_creation_with_empty_payload(self, booking_service):
        """
        Test for creating booking with empty payload.
        :param booking_service: An instance of BookingService.
        """
        booking_service.create_booking({}, expected_status = 500)
