import responses
from vkinfo.util.parsers import parse_friends_df



@responses.activate
def test_get_friends_mock(vk):
    """test get.friends method with mock data"""
    expected_ids = [1, 2, 3, 4, 5]
    responses.add(
        responses.GET,
        "https://api.vk.com/method/friends.get",
        json={"response": {"count": len(expected_ids), "items": expected_ids}},
        status=200,
    )

    resp_ids = vk.method_execute(
        method="friends.get",
        response_raw=True
    )
    assert resp_ids['response'] == {"count": len(expected_ids), "items": expected_ids}


def test_api(vk):
    """test connection to vk api"""

    assert vk.token_validation()


def test_get_friends(vk):
    """test get method with additional fields values"""

    user_info = vk.method_execute(method='users.get', values={"user_id": 1, 'fields': 'city'})
    assert isinstance(user_info, list)
    assert user_info[0]['city']['id'] == 2
    assert user_info[0]['id'] == 1
