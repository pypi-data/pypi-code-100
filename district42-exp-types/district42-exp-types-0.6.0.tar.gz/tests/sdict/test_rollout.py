from baby_steps import given, then, when

from district42_exp_types.sdict import rollout


def test_rollout_empty():
    with given:
        val = {}

    with when:
        res = rollout(val)

    with then:
        assert res == {}


def test_rollout_flat():
    with given:
        val = {
            "id": 1,
            "name": "Bob"
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "id": 1,
            "name": "Bob"
        }


def test_rollout_nested():
    with given:
        val = {
            "id": 1,
            "name": "Bob",
            "friend.id": 2,
            "friend.name": "Alice",
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "id": 1,
            "name": "Bob",
            "friend": {
                "id": 2,
                "name": "Alice"
            }
        }


def test_rollout_deep_nested():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            "result.friend.id": 2,
            "result.friend.name": "Alice",
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                "id": 1,
                "name": "Bob",
                "friend": {
                    "id": 2,
                    "name": "Alice"
                }
            }
        }


def test_rollout_deep_nested_dict():
    with given:
        val = {
            "result.id": 1,
            "result.name": "Bob",
            "result.friend": {
                "id": 2
            },
            "result.friend.name": "Alice",
        }

    with when:
        res = rollout(val)

    with then:
        assert res == {
            "result": {
                "id": 1,
                "name": "Bob",
                "friend": {
                    "id": 2,
                    "name": "Alice"
                }
            }
        }
