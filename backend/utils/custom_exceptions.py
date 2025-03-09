class InvalidURLException(Exception):
    """Exception raised for invalid URLs."""
    def __init__(self, message="Invalid File URL"):
        self.message = message
        super().__init__(self.message)
