from aiohttp import ClientResponse


class HTTPException(Exception):
    def __init__(self, response: ClientResponse, error: str, message: str) -> None:
        self.response: ClientResponse = response
        self.error: str = error
        self.message: str = message

        fmt = '{0.status} {1}: {2}'
        super().__init__(fmt.format(self.response, self.error, self.message))


class BadRequest(HTTPException):
    """Exception for status code 400"""


class Unauthorized(HTTPException):
    """Exception for status code 401"""


class Forbidden(HTTPException):
    """Exception for status code 403"""


class NotFound(HTTPException):
    """Exception for status code 404"""

