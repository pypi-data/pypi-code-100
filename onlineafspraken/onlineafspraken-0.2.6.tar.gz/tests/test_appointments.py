from onlineafspraken.api.appointment import get_appointments


def test_get_appointments(agenda_id):

    appointments = get_appointments(agenda_id)

    assert appointments
