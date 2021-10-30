import pytest

from fedeproxy.activitypub.base_activity import ActivityObject


def test_base_activity_init():
    instance = ActivityObject(id="a", type="b")
    assert hasattr(instance, "id")
    assert hasattr(instance, "type")


def test_init_extra_fields():
    with pytest.raises(TypeError) as e:
        ActivityObject(id="a", type="b", fish="c")
    assert e.match("unexpected keyword argument 'fish'")
