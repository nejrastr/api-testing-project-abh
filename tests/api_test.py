import pytest
from APIUtils.booking_service import BookingService
from data.test_data import USER_DATA, BOOKING_DATA, UPDATE_BOOKING_DATA

class TestAPI:
    @classmethod
    def setup_class(cls):
        service = BookingService()
        res = service.health_check()
        if res.status_code != 201:
            pytest.exit(f"CRITICAL: API Health Check failed (Status: {res.status_code}). Stopping suite.")

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = BookingService()
        self.service.create_api_token(USER_DATA)
        self.booking_data = BOOKING_DATA
        self.update_booking_data = UPDATE_BOOKING_DATA

    @pytest.mark.dependency(depends=["health"])
    def test_get_booking_ids(self):
        res = self.service.get_booking_ids()
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0

    @pytest.mark.dependency(depends=["health"])
    def test_get_booking_ids_by_name_and_surname(self):
        res = self.service.get_booking_ids(firstname=self.booking_data["firstname"],
        lastname=self.booking_data["lastname"])
        assert res.status_code == 200

    @pytest.mark.dependency(depends=["health"])
    def test_get_booking_checkin_checkout(self):
        res = self.service.get_booking_ids(checkin=self.booking_data["bookingdates"]["checkin"], checkout=self.booking_data["bookingdates"]["checkout"])
        assert res.status_code == 200

    @pytest.mark.dependency(depends=["health"])
    def test_get_booking(self):
        all_bookings = self.service.get_booking_ids()
        booking_id = all_bookings.json()[0]["bookingid"]
        res = self.service.get_booking(booking_id)
        assert res.status_code == 200

    @pytest.mark.dependency(depends=["health"])
    def test_create_booking(self):
        booking_res = self.service.create_booking(self.booking_data)
        assert booking_res.status_code == 200
        booking_id = booking_res.json()["bookingid"]
        new_booking = self.service.get_booking(booking_id)
        assert new_booking.json() == self.booking_data

    @pytest.mark.dependency(depends=["health"])
    def test_update_booking(self):
        all_bookings = self.service.get_booking_ids()
        booking_id = all_bookings.json()[0]["bookingid"]
        updated_booking = self.service.update_booking(booking_id, self.update_booking_data)
        assert updated_booking.status_code == 200
        assert updated_booking.json() == self.update_booking_data

    @pytest.mark.dependency(depends=["health"])
    def test_partial_update_booking(self):

        all_bookings = self.service.get_booking_ids()
        booking_id = all_bookings.json()[0]["bookingid"]
        new_first_name = {"firstname": self.update_booking_data["firstname"]}
        updated_booking = self.service.update_booking_partial(booking_id, new_first_name)
        assert updated_booking.status_code == 200

    @pytest.mark.dependency(depends=["health"])
    def test_delete_booking(self):
        temp_booking = self.service.create_booking(self.booking_data).json()
        target_id = temp_booking["bookingid"]

        del_res = self.service.delete_booking(target_id)
        assert del_res.status_code == 201
        get_res = self.service.get_booking(target_id)
        assert get_res.status_code == 404












