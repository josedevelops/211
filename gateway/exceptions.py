class InvalidLocationAddress(Exception):
    def __init__(self, message: str = "Invalid Location Address"):
        self.message = message
        super().__init__(self.message)


class RequestServiceExceptions(Exception):
    def __init__(self, message: str = "Request service failed"):
        self.message = message
        super().__init__(self.message)


class PublisherException(Exception):
    def __init__(self, message: str = "Failed to publish event"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenException(Exception):
    def __init__(self, message: str = "Invalid or missing token"):
        self.message = message
        super().__init__(self.message)
