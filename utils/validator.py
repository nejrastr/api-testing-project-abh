class BookingValidator:
    @staticmethod
    def validate_booking(actual_data, expected_data):
        assert actual_data["firstname"] == expected_data["firstname"]
        assert actual_data["lastname"] == expected_data["lastname"]
        assert actual_data["totalprice"] == expected_data["totalprice"]
        assert actual_data["depositpaid"] == expected_data["depositpaid"]
        assert actual_data["bookingdates"]["checkin"] == expected_data["bookingdates"]["checkin"]
        assert actual_data["bookingdates"]["checkout"] == expected_data["bookingdates"]["checkout"]
        assert actual_data["additionalneeds"] == expected_data["additionalneeds"]



