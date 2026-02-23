import logging
from utils.validator import BookingValidator

logger = logging.getLogger(__name__)

class TestBookingActions:
    """
    Suite of tests covering the CRUD operations related to booking actions.
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
        data = booking_ids.json()
        assert isinstance(data, list), "Expected a list of bookings."
        assert len(data) > 0, "Booking IDs should not be empty."
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
        assert booking_ids.status_code == 200
        data = booking_ids.json()
        assert isinstance(data, list), "Expected a list of bookings."
        assert "bookingid" in data[0], f"Booking object missing 'bookingid' attribute."

    def test_get_booking(self, booking_service, existing_booking_id):
        """
        Test for fetching booking data by id.
        Steps:
        1. Fetch booking details by booking id.
        :param booking_service: An instance of BookingService.
        :param existing_booking_id: Booking id fetched from database.
        """
        logger.info("Fetch booking details by booking id.")
        booking_details = booking_service.get_booking(existing_booking_id)
        assert booking_details.status_code == 200

    def test_create_booking(self, booking_service, booking_payload):
        """
        Test for creating booking.
        Steps:
        1. Create a new booking.
        2. Verify status code and data structure.
        3. Verify that returned data matches submitted data.
        4. Get newly created booking.
        5. Verify that returned data from database matches submitted data.
        :param booking_service: An instance of BookingService.
        :param existing_booking_id: Booking id fetched from database.
        :param booking_payload: Test data for creating booking.
        """
        logger.info(f"Creating new booking: {booking_payload}")
        created_booking = booking_service.create_booking(booking_payload)

        logger.info("Verifying booking response contains booking id.")
        assert "bookingid" in created_booking.json(), "Booking response does not contain 'bookingid' attribute."
        logger.info("Verifying that returned data from response matches expected data.")
        BookingValidator.validate_booking(created_booking.json()["booking"], booking_payload)
        logger.info("Fetching booking details from API endpoint by newly created booking id.")
        new_id = created_booking.json()["bookingid"]
        new_booking = booking_service.get_booking(new_id)
        logger.info(f"Verifying that returned data from API endpoint matches submitted data, newly created booking data: {new_booking.json()}")
        BookingValidator.validate_booking(new_booking.json(), booking_payload)

    def test_update_booking(self, booking_service, existing_booking_id, update_payload):
       """
       Test for updating booking.
       Steps:
       1. Update booking by existing booking id.
       2. Verify status code and data structure.
       :param booking_service: An instance of BookingService.
       :param existing_booking_id: Booking id fetched from database.
       :param update_payload: Test data for updating booking.
       """
       logger.info(f"Updating booking: {update_payload}")
       updated_booking = booking_service.update_booking(existing_booking_id, update_payload)
       assert updated_booking.json() == update_payload

    def test_partial_update_booking(self, booking_service, update_payload, existing_booking_id):
        """
        Test for partial updating booking.
        :param booking_service: An instance of BookingService.
        :param update_payload: Test data for updating booking.
        :param existing_booking_id: Booking id fetched from database.
        Steps:
        1. Partially update booking by existing booking id.
        """
        new_first_name = {"firstname": update_payload["firstname"]}
        booking_service.update_booking_partial(existing_booking_id, new_first_name)



    def test_delete_booking(self, booking_service, booking_payload):
        """
        Steps:
        1. Create a new temp booking for deletion.
        2. Get temp booking id.
        3. Delete temp booking by id.
        2. Verify that booking is deleted from database successfully.

        """
        logger.info(f"Creating new temp booking for deletion: {booking_payload}")
        temp_booking = booking_service.create_booking(booking_payload).json()
        logger.info("Get temp booking id.")
        target_id = temp_booking["bookingid"]
        logger.info("Deleting temp booking...")
        booking_service.delete_booking(target_id)
        logger.info("Verifying that booking is successfully deleted from database.")

