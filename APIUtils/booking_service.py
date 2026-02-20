from RequestUtils.requests import Requests

class BookingService(Requests):
    def __init__(self):
        super().__init__()
    def create_api_token(self, test_user):
     response = self.post("/auth", json=test_user)
     if response.status_code == 200:
      token = response.json().get("token")
      self.session.headers.update({"Cookie": f"token={token}"})
     return response
    def get_booking_ids(self, **params):
        response = self.get("/booking", params=params)
        return response
    def get_booking(self, booking_id):
        response = self.get(f"/booking/{booking_id}")
        return response

    def create_booking(self, booking_data):
        response = self.post("/booking", json=booking_data)
        return response

    def update_booking(self, booking_id, booking_data):
        response = self.put(f"/booking/{booking_id}", json=booking_data)
        return response

    def update_booking_partial(self, booking_id, booking_data):
        response = self.patch(f"/booking/{booking_id}", json=booking_data)
        return response

    def delete_booking(self, booking_id):
        response = self.delete(f"/booking/{booking_id}")
        return response

    def health_check(self):
        response = self.get("/ping")
        return response