"""Users Class for calling 'users' API endpoint features."""
from restfly.endpoint import APIEndpoint


class Users(APIEndpoint):
    """'user's API endpoint"""

    _path = "users"

    def list(self):
        """GET action on 'users' API for a specific user ID"""
        return self._get().json()

    def get_user(self, uid: int):
        """GET a specific user."""
        _path = f"{self._path}/{uid}"
        return self._get().json()

    def add_user(self, **kwargs):
        """Add a user"""
        # Add parameters to payload
        payload = {}
        for key, value in kwargs.items():
            payload[key] = value

        return self._post(json=payload)
