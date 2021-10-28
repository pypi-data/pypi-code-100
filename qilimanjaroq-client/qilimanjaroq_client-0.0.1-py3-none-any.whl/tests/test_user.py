""" Tests methods for user """
from qilimanjaroq_client.user import User


def test_user_creation():
    user = User(id=1, username="test-user", api_key="000-3333")
    assert isinstance(user, User)
    print(user.__dict__)
    assert user.id == 1
    assert user.username == "test-user"
    assert user.api_key == "000-3333"
