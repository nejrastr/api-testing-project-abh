import logging

logger = logging.getLogger(__name__)

class TestBookingActions:
    shared_id = None
    """
    Suite of tests covering the CRUD operations related to booking actions.
    """
    def test_create_booking(self, booking_service, booking_payload):
        """
        Test for creating and validating booking.
        :param booking_service: An instance of BookingService.
        :param booking_payload: Booking service test data.
        """
        TestBookingActions.shared_id = booking_service.create_and_validate_booking(booking_payload)

    def test_get_booking(self, booking_service):
        """
        Test for fetching booking data by id.
        Steps:
        1. Fetch booking details by booking id.
        :param booking_service: An instance of BookingService.
        """
        target_id = TestBookingActions.shared_id
        logger.info("Fetch booking details by booking id.")
        booking_service.get_booking(target_id)

    def test_update_booking(self, booking_service, update_payload):
       """
       Test for updating booking.
       Steps:
       1. Update booking by existing booking id.
       2. Verify status code and data structure.
       :param booking_service: An instance of BookingService.
       :param update_payload: Test data for updating booking.
       """
       target_id = TestBookingActions.shared_id
       logger.info(f"Updating booking: {update_payload}")
       booking_service.update_booking(target_id, update_payload)

    def test_delete_booking(self, booking_service, booking_payload):
        """
        Steps:
        1. delete booking by booking id.
        2. Verify that booking is deleted from database successfully.

        """
        target_id = TestBookingActions.shared_id
        logger.info("Deleting temp booking...")
        booking_service.delete_booking(target_id)
        logger.info("Verifying that booking is successfully deleted from database.")
