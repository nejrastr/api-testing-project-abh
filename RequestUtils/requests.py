from dotenv import load_dotenv
import requests
import os
load_dotenv()

class Requests:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.session.verify = False
        self.base_api_url=os.getenv("BASE_API_URL")

    def get(self, endpoint, **kwargs):
        return self.session.get(self.base_api_url+endpoint, **kwargs)
    def post(self, endpoint, **kwargs):
        return self.session.post(self.base_api_url+endpoint, **kwargs)
    def put(self, endpoint, **kwargs):
        return self.session.put(self.base_api_url+endpoint, **kwargs)
    def delete(self, endpoint, **kwargs):
        return self.session.delete(self.base_api_url+endpoint, **kwargs)
    def patch(self, endpoint, **kwargs):
        return self.session.patch(self.base_api_url+endpoint, **kwargs)
