from datetime import datetime
from typing import Optional, Dict, List

from onlineafspraken.schema.response import OnlineAfsprakenBase


class AppointmentSchema(OnlineAfsprakenBase):
    id: int
    name: str
    description: Optional[str]
    start_time: datetime
    finish_time: datetime
    blocked_time: datetime
    capacity: int
    appointment_type_id: Optional[int]
    customer_id: Optional[int]
    customer_name: Optional[str]
    status: int
    resources: dict
    create_time: datetime
    update_time: datetime


class ConfirmAppointmentSchema(OnlineAfsprakenBase):
    confirmed: int


class SetAppointmentSchema(OnlineAfsprakenBase):
    id: int
    status: int


class CancelAppointmentResponse(OnlineAfsprakenBase):
    pass


class ConfirmAppointmentResponse(OnlineAfsprakenBase):
    appointment: ConfirmAppointmentSchema


class GetAppointmentsResponse(OnlineAfsprakenBase):
    appointment: List[AppointmentSchema]


class GetAppointmentResponse(OnlineAfsprakenBase):
    appointment: AppointmentSchema


class SetAppointmentResponse(OnlineAfsprakenBase):
    objects: Optional[Dict[str, SetAppointmentSchema]]
