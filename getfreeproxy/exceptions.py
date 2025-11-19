from typing import Optional


class APIError(Exception):
    def __init__(self, status_code: Optional[int], message: str, raw_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.raw_body = raw_body


class InvalidAPIKey(APIError):
    pass


class NetworkError(Exception):
    pass


class TimeoutError(Exception):
    pass


class ParseError(Exception):
    pass
