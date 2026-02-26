import requests
import logging

logger = logging.getLogger(__name__)

class Requests:
    """
        A generic HTTP client wrapper around the requests.Session library.
        This class provides a reusable interface for making HTTP requests
        with a persistent session, a common base URL, and shared headers.
        """
    def __init__(self, base_url: str, headers: dict = None, verify: bool = True):
        """
        Initialize the Requests session.
        :param base_url: The base URL for the requests session.
        :param headers: a dictionary of headers to add to the session.
        :param verify: Verify SSL certificates.
        """
        self.session = requests.Session()
        self.session.verify = verify
        self.base_api_url = base_url
        if headers:
            self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        """
        Builds the API URL for the requests session.
        :param endpoint: Resource endpoint to send the request to.
        :return: Full API URL.
        """
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_api_url}{endpoint}"

    def request(self, method: str, endpoint: str, **kwargs) ->requests.Response:
        """
        Centralized request handler.
        :param method: Method name to send the request to.
        :param endpoint: API endpoint to send the request to.
        :param kwargs: Additional keyword arguments to send in the request.
        """
        url = self._build_url(endpoint)
        logger.info(f"Sending {method} request to {url}")
        response = self.session.request(method=method, url=url, **kwargs)
        return response

    def get(self, endpoint:str, **kwargs) ->requests.Response:
        """
        Sends a GET request to the base URL.
        :param endpoint: The API endpoint to send the GET request to.
        :param kwargs: Additional keyword arguments to send in the GET request.
        :return: A requests.Response object.
        """
        return self.request(method="GET", endpoint=endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) ->requests.Response:
        """
        Sends a POST request to the base URL.
        :param endpoint: The API endpoint to send the POST request to.
        :param kwargs: Additional keyword arguments to send in the POST request.
        :return: A requests.Response object.
        """
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint:str, **kwargs) -> requests.Response:
        """
        Sends a PUT request to the base URL.
        :param endpoint: The API endpoint to send the PUT request to.
        :param kwargs: Additional keyword arguments to send in the PUT request.
        :return: A requests.Response object.
        """
        return self.request(method="PUT", endpoint=endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) ->requests.Response:
        """
        Sends a DELETE request to the base URL.
        :param endpoint: The API endpoint to send the DELETE request to.
        :param kwargs: Additional keyword arguments to send in the DELETE request.
        :return: A requests.Response object.
        """
        return self.request(method="DELETE", endpoint=endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) ->requests.Response:
        """
        Sends a PATCH request to the base URL.
        :param endpoint: The API endpoint to send the PATCH request to.
        :param kwargs: Additional keyword arguments to send in the PATCH request.
        :return: A requests.Response object.
        """
        return self.request(method="PATCH", endpoint=endpoint, **kwargs)
