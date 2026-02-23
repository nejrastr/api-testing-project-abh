import requests

class Requests:
    """
        A generic HTTP client wrapper around the requests.Session library.
        This class provides a reusable interface for making HTTP requests
        with a persistent session, a common base URL, and shared headers.
        """
    def __init__(self, base_url: str, headers: dict = None):
        """
        Initialize the Requests session.
        :param base_url: The base URL for the requests session.
        :param headers: a dictionary of headers to add to the session.
        """
        self.session = requests.Session()
        self.session.verify = False
        self.base_api_url=base_url
        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint:str, **kwargs) ->requests.Response:
        """
        Sends a GET request to the base URL.
        :param endpoint: The API endpoint to send the GET request to.
        :param kwargs: Additional keyword arguments to send in the GET request.
        :return: A requests.Response object.
        """

        return self.session.get(f"{self.base_api_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs) ->requests.Response:
        """
        Sends a POST request to the base URL.
        :param endpoint: The API endpoint to send the POST request to.
        :param kwargs: Additional keyword arguments to send in the POST request.
        :return: A requests.Response object.
        """
        return self.session.post(f"{self.base_api_url}{endpoint}", **kwargs)

    def put(self, endpoint:str, **kwargs) -> requests.Response:
        """
        Sends a PUT request to the base URL.
        :param endpoint: The API endpoint to send the PUT request to.
        :param kwargs: Additional keyword arguments to send in the PUT request.
        :return: A requests.Response object.
        """
        return self.session.put(f"{self.base_api_url}{endpoint}", **kwargs)

    def delete(self, endpoint: str, **kwargs) ->requests.Response:
        """
        Sends a DELETE request to the base URL.
        :param endpoint: The API endpoint to send the DELETE request to.
        :param kwargs: Additional keyword arguments to send in the DELETE request.
        :return: A requests.Response object.
        """
        return self.session.delete(f"{self.base_api_url}{endpoint}", **kwargs)

    def patch(self, endpoint: str, **kwargs) ->requests.Response:
        """
        Sends a PATCH request to the base URL.
        :param endpoint: The API endpoint to send the PATCH request to.
        :param kwargs: Additional keyword arguments to send in the PATCH request.
        :return: A requests.Response object.
        """
        return self.session.patch(f"{self.base_api_url}{endpoint}", **kwargs)
