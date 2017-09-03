"""Submodule of keepasshttp, providing custom exceptions."""


class RequestFailed(Exception):
    """Custom Exception, representing a failed request."""

    def __init__(self, message, response):
        """Initialize a new RequestFailed exception."""
        Exception.__init__(self, message)
        self.response = response
