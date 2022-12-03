class BadRequest(Exception):
    def __init__(self, message=None, loc=None):
        super().__init__(message)
        self.message = message
        self.loc = loc
