from collections import namedtuple

import attr
import pytest

from classical.fields.functions import (
    are_analogous, copy_to_class,
)


def test_are_analogous():
    FieldedNT = namedtuple('FieldedNT', ('size', 'color'))

    @attr.s
    class FieldedAttrs:
        size = attr.ib()
        color = attr.ib()

    @attr.s
    class FieldedAttrsExtended(FieldedAttrs):
        new_attr = attr.ib()

    assert are_analogous(FieldedNT, FieldedAttrs)
    assert not are_analogous(FieldedNT, FieldedAttrsExtended)
    assert are_analogous(FieldedNT, FieldedAttrsExtended, exclude_names=('new_attr',))


def test_copy_to_class():
    @attr.s
    class FieldedAttrs:
        size = attr.ib(default=99)
        color = attr.ib(default='white')

    @attr.s
    class FieldedAttrsExtended(FieldedAttrs):
        new_attr = attr.ib(default='default')

    super_obj = FieldedAttrs(size=12, color='green')
    sub_obj = FieldedAttrsExtended(size=12, color='green', new_attr='qwerty')

    new_sub_obj = copy_to_class(super_obj, FieldedAttrsExtended, ignore_missing=True)
    assert new_sub_obj == FieldedAttrsExtended(size=12, color='green', new_attr='default')
    with pytest.raises(ValueError):
        copy_to_class(super_obj, FieldedAttrsExtended)

    new_sub_obj = copy_to_class(super_obj, FieldedAttrsExtended, defaults=dict(new_attr='a'))
    assert new_sub_obj == FieldedAttrsExtended(size=12, color='green', new_attr='a')

    new_super_obj = copy_to_class(sub_obj, FieldedAttrs, ignore_extra=True)
    assert new_super_obj == FieldedAttrs(size=12, color='green')
    with pytest.raises(ValueError):
        copy_to_class(sub_obj, FieldedAttrs)
