#!/usr/bin/env python

"""Tests for `onlineafspraken` package."""
import datetime

from onlineafspraken.api import appointment, availability, customers, general
from onlineafspraken.schema.appointment import AppointmentSchema
from onlineafspraken.schema.availability import BookableTimeSchema


def test_get_bookable_days(agenda_id, appointment_type_id):
    response = availability.get_bookable_days(
        agenda_id=agenda_id,
        appointment_type_id=appointment_type_id,
        start_date="2021-07-12",
        end_date="2021-12-31",
    )
    assert isinstance(response, list)


def test_get_bookable_times(agenda_id, appointment_type_id):
    response = availability.get_bookable_times(
        agenda_id=agenda_id, appointment_type_id=appointment_type_id, date="2021-11-06"
    )
    assert isinstance(response[0], BookableTimeSchema)


def test_set_customer():
    c = customers.set_customer("john", "doe", "johbdoe@test.com")
    pass


def test_get_customers():
    c = customers.get_customers()
    pass


def test_get_customer():
    c = customers.get_customer(26142790)
    pass


def test_appointment():

    types = general.get_appointment_types()

    agendas = general.get_agendas()

    agenda = agendas[0]
    appointment_type = types[0]

    bookable_times = availability.get_bookable_times(
        agenda_id=agenda.id,
        appointment_type_id=appointment_type.id,
        date=datetime.date.today(),
    )

    first_slot = bookable_times[0]

    customer = customers.set_customer(first_name="Py", last_name="Test", email="py@jelmert.nl")

    assert customer.id

    result = appointment.set_appointment(
        agenda_id=agenda.id,
        appointment_type_id=appointment_type.id,
        date=first_slot.date,
        start_time=first_slot.start_time,
        customer_id=customer.id,
        description="Test 1234",
        name="Test Appointment",
    )

    assert result.id

    obj: AppointmentSchema = appointment.get_appointment(result.id)

    assert obj.id == result.id

    appointment.cancel_appointment(result.id, mode='company')

    appointment.remove_appointment(result.id)
