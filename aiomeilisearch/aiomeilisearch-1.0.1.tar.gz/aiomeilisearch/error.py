from typing import Dict, Any
try:
    import ujson as json
except:
    import json

class AioMeiliSearchError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'MeiliSearchError. Error message: {self.message}.'


class AioMeiliSearchApiError(AioMeiliSearchError):
    def __init__(self, error: str, response: Dict[str, Any]) -> None:
        self.error_code = None
        self.error_link = None
        if response and isinstance(response, dict):
            self.message = response.get('message')
            self.error_code = response.get('errorCode')
            self.error_link = response.get('errorLink')
        else:
            self.message = error
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.error_code and self.error_link:
            return f'Error code: {self.error_code}. Error message: {self.message}. Error documentation: {self.error_link}'
        else:
            return f'MeiliSearchApiError. {self.message}'

class AioMeiliSearchTimeoutError(AioMeiliSearchError):
    """Error when MeiliSearch operation takes longer than expected"""
    def __str__(self) -> str:
        return f'Error message: {self.message}.'