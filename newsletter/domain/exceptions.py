class BaseDomainError(Exception):
    def __init__(self, message: str):
        self._message = message
        super().__init__(message)

    @property
    def message(self) -> str:
        return self._message
