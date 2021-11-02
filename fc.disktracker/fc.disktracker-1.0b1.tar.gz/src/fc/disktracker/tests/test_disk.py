from fc.disktracker.disk import Disk


def test_disks_can_be_compared_and_sorted_by_value():
    disk1 = Disk(manufacturer='Samsung', model='the big one', serial='12345')
    assert disk1.manufacturer == 'Samsung'
    assert disk1.model == 'the big one'
    assert disk1.serial == '12345'

    # Trivial cases
    assert disk1 == disk1
    assert [disk1] == list(sorted([disk1]))

    # Add one more disk
    disk2 = Disk(manufacturer='HGST', model='a really big one', serial='23456')
    assert disk1 != disk2
    assert [disk2, disk1] == list(sorted([disk1, disk2]))
